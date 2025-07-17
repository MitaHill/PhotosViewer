#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能位置计算组件
Intelligent Position Calculator Component
"""

import math
import time


class PositionCalculator:
    """智能位置计算器"""

    def __init__(self, parent):
        """
        初始化位置计算器

        Args:
            parent: 父对象（ImageViewer实例）
        """
        self.parent = parent

        # 位置计算参数
        self.avoidance_distance = 100  # 避让距离（像素）
        self.min_edge_distance = 20  # 距离边缘的最小距离
        self.position_history = []  # 位置历史记录
        self.max_history = 10  # 最大历史记录数

        # 性能优化
        self.last_update_time = 0
        self.update_threshold = 50  # 更新间隔（毫秒）
        self.last_mouse_pos = (0, 0)

        # 智能预测
        self.mouse_velocity = (0, 0)
        self.velocity_samples = []
        self.max_velocity_samples = 5

        # 位置偏好
        self.preferred_positions = [
            'top_left', 'top_right', 'bottom_left', 'bottom_right'
        ]
        self.current_position_preference = 0

    def update_position_if_needed(self, mouse_x, mouse_y):
        """
        根据需要更新悬浮框位置

        Args:
            mouse_x: 鼠标X坐标
            mouse_y: 鼠标Y坐标
        """
        current_time = time.time() * 1000  # 转为毫秒

        # 节流控制
        if current_time - self.last_update_time < self.update_threshold:
            return

        # 更新鼠标速度
        self._update_mouse_velocity(mouse_x, mouse_y, current_time)

        # 获取悬浮框当前位置
        if not hasattr(self.parent, 'overlay_manager') or not self.parent.overlay_manager.overlay_exists():
            return

        overlay_bounds = self.parent.overlay_manager.get_bounds()
        overlay_x, overlay_y, overlay_width, overlay_height = overlay_bounds

        # 计算鼠标与悬浮框的距离
        distance = self._calculate_distance_to_overlay(
            mouse_x, mouse_y, overlay_x, overlay_y, overlay_width, overlay_height
        )

        # 只有距离小于阈值时才重新计算位置
        if distance < self.avoidance_distance:
            new_position = self._calculate_optimal_position(mouse_x, mouse_y)
            if new_position:
                new_x, new_y = new_position

                # 检查新位置是否确实更好
                if self._is_position_better(new_x, new_y, overlay_x, overlay_y, mouse_x, mouse_y):
                    self.parent.overlay_manager.update_position(new_x, new_y, animate=True)
                    self._add_position_to_history(new_x, new_y)

        self.last_update_time = current_time
        self.last_mouse_pos = (mouse_x, mouse_y)

    def _update_mouse_velocity(self, mouse_x, mouse_y, current_time):
        """
        更新鼠标速度信息

        Args:
            mouse_x, mouse_y: 当前鼠标位置
            current_time: 当前时间（毫秒）
        """
        if self.last_mouse_pos != (0, 0) and hasattr(self, 'last_update_time'):
            time_delta = current_time - self.last_update_time
            if time_delta > 0:
                dx = mouse_x - self.last_mouse_pos[0]
                dy = mouse_y - self.last_mouse_pos[1]

                # 计算速度（像素/毫秒）
                velocity_x = dx / time_delta
                velocity_y = dy / time_delta

                # 添加到速度样本
                self.velocity_samples.append((velocity_x, velocity_y))
                if len(self.velocity_samples) > self.max_velocity_samples:
                    self.velocity_samples.pop(0)

                # 计算平均速度
                if self.velocity_samples:
                    avg_vx = sum(v[0] for v in self.velocity_samples) / len(self.velocity_samples)
                    avg_vy = sum(v[1] for v in self.velocity_samples) / len(self.velocity_samples)
                    self.mouse_velocity = (avg_vx, avg_vy)

    def _calculate_distance_to_overlay(self, mouse_x, mouse_y, overlay_x, overlay_y, overlay_width, overlay_height):
        """
        计算鼠标到悬浮框的最短距离

        Args:
            mouse_x, mouse_y: 鼠标坐标
            overlay_x, overlay_y: 悬浮框位置
            overlay_width, overlay_height: 悬浮框尺寸

        Returns:
            float: 最短距离
        """
        # 计算悬浮框中心点
        center_x = overlay_x + overlay_width / 2
        center_y = overlay_y + overlay_height / 2

        # 计算鼠标到中心点的距离
        distance = math.sqrt((mouse_x - center_x) ** 2 + (mouse_y - center_y) ** 2)

        return distance

    def _calculate_optimal_position(self, mouse_x, mouse_y):
        """
        计算最优的悬浮框位置

        Args:
            mouse_x, mouse_y: 鼠标坐标

        Returns:
            tuple: 最优位置 (x, y) 或 None
        """
        canvas_width = self.parent.canvas.winfo_width()
        canvas_height = self.parent.canvas.winfo_height()

        if canvas_width < 100 or canvas_height < 100:
            return None

        overlay_width = 200
        overlay_height = 80

        # 预测鼠标未来位置（基于速度）
        predicted_x, predicted_y = self._predict_mouse_position(mouse_x, mouse_y, 200)  # 预测200ms后

        # 计算候选位置
        candidates = self._generate_position_candidates(
            predicted_x, predicted_y, canvas_width, canvas_height, overlay_width, overlay_height
        )

        # 评估每个候选位置
        best_position = self._evaluate_positions(candidates, predicted_x, predicted_y)

        return best_position

    def _predict_mouse_position(self, current_x, current_y, time_ahead_ms):
        """
        基于当前速度预测鼠标未来位置

        Args:
            current_x, current_y: 当前位置
            time_ahead_ms: 预测时间（毫秒）

        Returns:
            tuple: 预测位置
        """
        if not self.mouse_velocity or self.mouse_velocity == (0, 0):
            return current_x, current_y

        vx, vy = self.mouse_velocity

        # 预测位置
        predicted_x = current_x + vx * time_ahead_ms
        predicted_y = current_y + vy * time_ahead_ms

        # 限制在画布范围内
        canvas_width = self.parent.canvas.winfo_width()
        canvas_height = self.parent.canvas.winfo_height()

        predicted_x = max(0, min(predicted_x, canvas_width))
        predicted_y = max(0, min(predicted_y, canvas_height))

        return predicted_x, predicted_y

    def _generate_position_candidates(self, mouse_x, mouse_y, canvas_width, canvas_height, overlay_width,
                                      overlay_height):
        """
        生成候选位置列表

        Args:
            mouse_x, mouse_y: 鼠标位置
            canvas_width, canvas_height: 画布尺寸
            overlay_width, overlay_height: 悬浮框尺寸

        Returns:
            list: 候选位置列表
        """
        candidates = []

        # 四个角落位置
        positions = {
            'top_left': (self.min_edge_distance, self.min_edge_distance),
            'top_right': (canvas_width - overlay_width - self.min_edge_distance, self.min_edge_distance),
            'bottom_left': (self.min_edge_distance, canvas_height - overlay_height - self.min_edge_distance),
            'bottom_right': (canvas_width - overlay_width - self.min_edge_distance,
                             canvas_height - overlay_height - self.min_edge_distance)
        }

        # 根据鼠标位置智能排序
        mouse_in_left = mouse_x < canvas_width / 2
        mouse_in_top = mouse_y < canvas_height / 2

        if mouse_in_left and mouse_in_top:
            # 鼠标在左上，优先选择右下、右上、左下
            priority = ['bottom_right', 'top_right', 'bottom_left', 'top_left']
        elif not mouse_in_left and mouse_in_top:
            # 鼠标在右上，优先选择左下、左上、右下
            priority = ['bottom_left', 'top_left', 'bottom_right', 'top_right']
        elif mouse_in_left and not mouse_in_top:
            # 鼠标在左下，优先选择右上、右下、左上
            priority = ['top_right', 'bottom_right', 'top_left', 'bottom_left']
        else:
            # 鼠标在右下，优先选择左上、左下、右上
            priority = ['top_left', 'bottom_left', 'top_right', 'bottom_right']

        # 按优先级添加候选位置
        for pos_name in priority:
            if pos_name in positions:
                candidates.append(positions[pos_name])

        # 添加一些中间位置作为备选
        mid_x = (canvas_width - overlay_width) / 2
        mid_y = (canvas_height - overlay_height) / 2

        if mouse_x < canvas_width / 3:
            # 鼠标在左侧，添加右侧中间位置
            candidates.append((canvas_width - overlay_width - self.min_edge_distance, mid_y))
        elif mouse_x > canvas_width * 2 / 3:
            # 鼠标在右侧，添加左侧中间位置
            candidates.append((self.min_edge_distance, mid_y))

        if mouse_y < canvas_height / 3:
            # 鼠标在上方，添加下方中间位置
            candidates.append((mid_x, canvas_height - overlay_height - self.min_edge_distance))
        elif mouse_y > canvas_height * 2 / 3:
            # 鼠标在下方，添加上方中间位置
            candidates.append((mid_x, self.min_edge_distance))

        return candidates

    def _evaluate_positions(self, candidates, mouse_x, mouse_y):
        """
        评估候选位置并选择最佳位置

        Args:
            candidates: 候选位置列表
            mouse_x, mouse_y: 鼠标位置

        Returns:
            tuple: 最佳位置或None
        """
        if not candidates:
            return None

        best_position = None
        best_score = -1

        for x, y in candidates:
            score = self._calculate_position_score(x, y, mouse_x, mouse_y)
            if score > best_score:
                best_score = score
                best_position = (x, y)

        return best_position

    def _calculate_position_score(self, pos_x, pos_y, mouse_x, mouse_y):
        """
        计算位置评分

        Args:
            pos_x, pos_y: 候选位置
            mouse_x, mouse_y: 鼠标位置

        Returns:
            float: 位置评分（越高越好）
        """
        score = 0

        # 1. 距离鼠标的距离（越远越好）
        distance = math.sqrt((pos_x - mouse_x) ** 2 + (pos_y - mouse_y) ** 2)
        distance_score = min(distance / 200, 1.0) * 40  # 最高40分
        score += distance_score

        # 2. 避免与历史位置重复（鼓励位置变化）
        history_penalty = 0
        for hist_x, hist_y in self.position_history[-3:]:  # 检查最近3个位置
            hist_distance = math.sqrt((pos_x - hist_x) ** 2 + (pos_y - hist_y) ** 2)
            if hist_distance < 50:  # 如果太接近历史位置
                history_penalty += 10
        score -= history_penalty

        # 3. 边缘位置偏好（角落位置加分）
        canvas_width = self.parent.canvas.winfo_width()
        canvas_height = self.parent.canvas.winfo_height()

        # 距离边缘的距离
        edge_distance = min(
            pos_x, pos_y,
            canvas_width - pos_x - 200,  # 200是悬浮框宽度
            canvas_height - pos_y - 80  # 80是悬浮框高度
        )

        if edge_distance < 30:  # 接近边缘
            score += 20

        # 4. 对角线位置偏好（与鼠标在对角）
        mouse_in_left = mouse_x < canvas_width / 2
        mouse_in_top = mouse_y < canvas_height / 2
        pos_in_left = pos_x < canvas_width / 2
        pos_in_top = pos_y < canvas_height / 2

        if mouse_in_left != pos_in_left and mouse_in_top != pos_in_top:
            score += 15  # 对角线位置加分

        return score

    def _is_position_better(self, new_x, new_y, current_x, current_y, mouse_x, mouse_y):
        """
        判断新位置是否比当前位置更好

        Args:
            new_x, new_y: 新位置
            current_x, current_y: 当前位置
            mouse_x, mouse_y: 鼠标位置

        Returns:
            bool: 新位置是否更好
        """
        # 计算移动距离
        move_distance = math.sqrt((new_x - current_x) ** 2 + (new_y - current_y) ** 2)

        # 如果移动距离太小，不值得移动
        if move_distance < 30:
            return False

        # 计算新旧位置的评分
        new_score = self._calculate_position_score(new_x, new_y, mouse_x, mouse_y)
        current_score = self._calculate_position_score(current_x, current_y, mouse_x, mouse_y)

        # 新位置必须明显更好才移动（避免频繁移动）
        return new_score > current_score + 10

    def _add_position_to_history(self, x, y):
        """
        添加位置到历史记录

        Args:
            x, y: 位置坐标
        """
        self.position_history.append((x, y))
        if len(self.position_history) > self.max_history:
            self.position_history.pop(0)

    def set_avoidance_distance(self, distance):
        """
        设置避让距离

        Args:
            distance: 避让距离（像素）
        """
        self.avoidance_distance = max(50, min(200, distance))
        print(f"避让距离设置为: {self.avoidance_distance}px")

    def set_update_threshold(self, threshold_ms):
        """
        设置更新间隔阈值

        Args:
            threshold_ms: 间隔时间（毫秒）
        """
        self.update_threshold = max(10, min(200, threshold_ms))
        print(f"位置更新间隔设置为: {self.update_threshold}ms")

    def clear_history(self):
        """清空位置历史"""
        self.position_history.clear()
        self.velocity_samples.clear()
        self.mouse_velocity = (0, 0)

    def get_statistics(self):
        """
        获取位置计算统计信息

        Returns:
            dict: 统计信息
        """
        return {
            'avoidance_distance': self.avoidance_distance,
            'update_threshold': self.update_threshold,
            'position_history_count': len(self.position_history),
            'mouse_velocity': self.mouse_velocity,
            'velocity_samples_count': len(self.velocity_samples)
        }