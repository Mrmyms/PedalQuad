# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt, pyqtSignal, QSize, QTimer, QRectF, QPoint
from PyQt5.QtGui import QPainter, QColor, QPen, QPainterPath
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QScrollArea, QFrame, QSizePolicy, 
                             QSlider, QComboBox, QCheckBox)

class LinearKnobWidget(QWidget):
    valueChanged = pyqtSignal(float)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(60, 60)
        self.value = 0.0 # 0.0 to 1.0
        self._is_dragging = False
        self._last_y = 0
        
    def setValue(self, val):
        self.value = max(0.0, min(1.0, val))
        self.update()
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._is_dragging = True
            self._last_y = event.y()
            
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._is_dragging = False
            
    def mouseMoveEvent(self, event):
        if self._is_dragging:
            dy = self._last_y - event.y()
            # Sensitivity: 100 pixels for full range
            self.value += dy / 100.0
            self.value = max(0.0, min(1.0, self.value))
            self._last_y = event.y()
            self.valueChanged.emit(self.value)
            self.update()
            
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        rect = QRectF(5, 5, 50, 50)
        
        # Draw background circle
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("#2a2a35"))
        painter.drawEllipse(rect)
        
        # Draw arc background
        pen_bg = QPen(QColor("#111115"))
        pen_bg.setWidth(4)
        pen_bg.setCapStyle(Qt.RoundCap)
        painter.setPen(pen_bg)
        painter.setBrush(Qt.NoBrush)
        painter.drawArc(rect, -45 * 16, 270 * 16)
        
        # Draw value arc
        pen_val = QPen(QColor("#00ffff"))
        pen_val.setWidth(4)
        pen_val.setCapStyle(Qt.RoundCap)
        painter.setPen(pen_val)
        span_angle = int(-270 * self.value * 16)
        painter.drawArc(rect, 225 * 16, span_angle)
        
        # Draw indicator line
        painter.translate(rect.center())
        painter.rotate(-135 + 270 * self.value)
        pen_ind = QPen(QColor("#00ffff"))
        pen_ind.setWidth(2)
        painter.setPen(pen_ind)
        painter.drawLine(0, -10, 0, -20)


class Knob(QWidget):
    valueChanged = pyqtSignal(float)
    
    def __init__(self, name, min_val, max_val, default_val, current_val):
        super().__init__()
        self.min_val = min_val
        self.max_val = max_val
        self.name = name
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(5, 5, 5, 5)
        
        self.dial = LinearKnobWidget()
        self._set_dial_value(current_val)
        self.dial.valueChanged.connect(self._on_dial_change)
        
        self.label = QLabel(name)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color: #00ffff; font-size: 10px; font-weight: bold;")
        
        self.val_label = QLabel(f"{current_val:.2f}")
        self.val_label.setAlignment(Qt.AlignCenter)
        self.val_label.setStyleSheet("color: white; font-size: 10px;")
        
        layout.addWidget(self.dial, alignment=Qt.AlignHCenter)
        layout.addWidget(self.label)
        layout.addWidget(self.val_label)
        
    def _set_dial_value(self, val):
        if self.max_val > self.min_val:
            normalized = (val - self.min_val) / (self.max_val - self.min_val)
            self.dial.setValue(normalized)
        
    def _on_dial_change(self, normalized):
        actual_val = self.min_val + normalized * (self.max_val - self.min_val)
        self.val_label.setText(f"{actual_val:.2f}")
        self.valueChanged.emit(actual_val)

from PyQt5.QtWidgets import QCheckBox, QComboBox

class ToggleParam(QWidget):
    valueChanged = pyqtSignal(float)
    
    def __init__(self, name, current_val):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        
        self.checkbox = QCheckBox()
        self.checkbox.setStyleSheet("""
            QCheckBox::indicator {
                width: 40px;
                height: 20px;
                border-radius: 10px;
                border: 1px solid #333;
                background: #111;
            }
            QCheckBox::indicator:checked {
                background: #00ffff;
            }
        """)
        self.checkbox.setChecked(current_val > 0.5)
        self.checkbox.toggled.connect(self._on_toggle)
        
        self.label = QLabel(name)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color: #00ffff; font-size: 10px; font-weight: bold;")
        
        layout.addWidget(self.checkbox, alignment=Qt.AlignHCenter)
        layout.addWidget(self.label)
        
    def _on_toggle(self, checked):
        self.valueChanged.emit(1.0 if checked else 0.0)

class ComboParam(QWidget):
    valueChanged = pyqtSignal(float)
    
    def __init__(self, name, scale_points, current_val):
        super().__init__()
        self.scale_points = scale_points
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        
        self.combo = QComboBox()
        self.combo.setStyleSheet("background: #222; color: #fff; border: 1px solid #00ffff;")
        
        current_idx = 0
        for i, sp in enumerate(scale_points):
            self.combo.addItem(sp['label'])
            if abs(sp['value'] - current_val) < 0.001:
                current_idx = i
                
        self.combo.setCurrentIndex(current_idx)
        self.combo.currentIndexChanged.connect(self._on_change)
        
        self.label = QLabel(name)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color: #00ffff; font-size: 10px; font-weight: bold;")
        
        layout.addWidget(self.combo)
        layout.addWidget(self.label)
        
    def _on_change(self, idx):
        val = self.scale_points[idx]['value']
        self.valueChanged.emit(val)

class ParameterDrawer(QFrame):
    def __init__(self, host, parent=None):
        super().__init__(parent)
        self.host = host
        self.pluginId = None
        self.setFixedHeight(250)
        self.setStyleSheet("background-color: #1a1a24; border-top: 2px solid #00ffff;")
        
        self.layout = QVBoxLayout(self)
        
        # Header
        self.header = QHBoxLayout()
        self.title = QLabel("No Plugin Selected")
        self.title.setStyleSheet("color: white; font-size: 16px; font-weight: bold; border: none;")
        
        self.btn_bypass_drawer = QPushButton("ON")
        self.btn_bypass_drawer.setFixedSize(40, 24)
        self.btn_bypass_drawer.setStyleSheet("background-color: #00ffff; color: #000; border-radius: 12px; font-weight: bold;")
        self.btn_bypass_drawer.clicked.connect(self._toggle_bypass_drawer)
        self.is_active_drawer = True
        
        self.preset_combo = QComboBox()
        self.preset_combo.setStyleSheet("background: #222; color: #fff; border: 1px solid #00ffff; padding: 2px;")
        self.preset_combo.setFixedWidth(150)
        self.preset_combo.hide()
        self.preset_combo.activated.connect(self._on_preset_changed)
        
        self.btn_ui = QPushButton("SHOW NATIVE UI")
        self.btn_ui.setStyleSheet("background-color: #003333; color: #00ffff; border: 1px solid #00ffff; padding: 5px;")
        self.btn_ui.clicked.connect(self._show_ui)
        self.btn_close = QPushButton("X")
        self.btn_close.setFixedSize(30, 30)
        self.btn_close.setStyleSheet("background: transparent; color: white; border: none; font-size: 16px;")
        self.btn_close.clicked.connect(self.hide)
        
        self.header.addWidget(self.title)
        self.header.addWidget(self.btn_bypass_drawer)
        self.header.addWidget(self.preset_combo)
        self.header.addStretch()
        self.header.addWidget(self.btn_ui)
        self.header.addWidget(self.btn_close)
        
        # Scroll area for params
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("border: none; background: transparent;")
        self.param_container = QWidget()
        self.param_layout = QHBoxLayout(self.param_container)
        self.param_layout.setAlignment(Qt.AlignLeft)
        self.scroll.setWidget(self.param_container)
        
        self.layout.addLayout(self.header)
        self.layout.addWidget(self.scroll)
        self.hide()
        
    def set_plugin(self, pluginId, name):
        print(f"ParameterDrawer.set_plugin called for {pluginId} ({name})", flush=True)
        self.pluginId = pluginId
        self.title.setText(name)
        
        # Read current bypass state if possible
        try:
            info = self.host.get_plugin_info(pluginId)
            self.is_active_drawer = info.get('active', True) if info else True
        except:
            self.is_active_drawer = True
        self._update_drawer_bypass_style()
        
        # Load Presets
        self.preset_combo.blockSignals(True)
        self.preset_combo.clear()
        try:
            prog_count = self.host.get_program_count(pluginId)
            if prog_count > 0:
                for i in range(prog_count):
                    prog_name = self.host.get_program_name(pluginId, i)
                    self.preset_combo.addItem(prog_name)
                current_prog = self.host.get_current_program_index(pluginId)
                self.preset_combo.setCurrentIndex(current_prog)
                self.preset_combo.show()
            else:
                self.preset_combo.hide()
        except:
            self.preset_combo.hide()
        self.preset_combo.blockSignals(False)
        
        # Clear old params
        for i in reversed(range(self.param_layout.count())): 
            self.param_layout.itemAt(i).widget().setParent(None)
            
        param_count = self.host.get_parameter_count(pluginId)
        
        for p in range(param_count):
            p_info = self.host.get_parameter_info(pluginId, p)
            if p_info:
                p_name = p_info['name']
                ranges = self.host.get_parameter_ranges(pluginId, p)
                val = self.host.get_current_parameter_value(pluginId, p)
                p_data = self.host.get_parameter_data(pluginId, p)
                
                # Check for boolean/toggle
                is_boolean = (p_data['hints'] & 0x001) != 0
                scale_count = p_info['scalePointCount']
                
                if is_boolean:
                    widget = ToggleParam(p_name, val)
                elif scale_count > 0:
                    scale_points = []
                    for sp in range(scale_count):
                        sp_info = self.host.get_parameter_scalepoint_info(pluginId, p, sp)
                        scale_points.append(sp_info)
                    widget = ComboParam(p_name, scale_points, val)
                else:
                    widget = Knob(p_name, ranges['min'], ranges['max'], ranges['def'], val)
                    
                # Capture variables for lambda
                widget.valueChanged.connect(lambda v, pId=pluginId, paramId=p: self.host.set_parameter_value(pId, paramId, v))
                self.param_layout.addWidget(widget)
                
        print(f"Added {param_count} parameters. Showing drawer.", flush=True)
        self.show()
        
    def _on_preset_changed(self, idx):
        if self.pluginId is not None:
            self.host.set_program(self.pluginId, idx)
            # Re-read parameters after preset load
            QTimer.singleShot(100, lambda: self.set_plugin(self.pluginId, self.title.text()))

    def _show_ui(self):
        if self.pluginId is not None:
            self.host.show_custom_ui(self.pluginId, True)

    def _toggle_bypass_drawer(self):
        if self.pluginId is not None:
            self.is_active_drawer = not self.is_active_drawer
            self._update_drawer_bypass_style()
            self.host.set_drywet(self.pluginId, 1.0 if self.is_active_drawer else 0.0)
            
    def _update_drawer_bypass_style(self):
        if self.is_active_drawer:
            self.btn_bypass_drawer.setText("ON")
            self.btn_bypass_drawer.setStyleSheet("background-color: #00ffff; color: #000; border-radius: 12px; font-weight: bold;")
        else:
            self.btn_bypass_drawer.setText("OFF")
            self.btn_bypass_drawer.setStyleSheet("background-color: #333333; color: #aaa; border-radius: 12px; font-weight: bold;")


