import sys
import json
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QComboBox,
    QPushButton, QTextEdit, QLabel, QStyleFactory, QTabWidget, QGridLayout,
    QScrollArea, QMenuBar, QMenu, QFileDialog, QMessageBox, QLineEdit, QDateEdit,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QIcon, QPalette, QColor, QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
from pathlib import Path

class GraphWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure, self.ax = plt.subplots(figsize=(4, 3))
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def update_graph(self, categories, amounts, title, lang):
        self.ax.clear()
        self.ax.bar(categories, amounts, color='#005A9E')
        self.ax.set_title(title, fontsize=12, color='#000000')
        self.ax.set_xlabel('Categories' if lang == 'en' else 'دسته‌بندی‌ها' if lang == 'fa' else '类别' if lang == 'zh' else 'Категории', fontsize=10, color='#000000')
        self.ax.set_ylabel('Amount' if lang == 'en' else 'مقدار' if lang == 'fa' else '金额' if lang == 'zh' else 'Сумма', fontsize=10, color='#000000')
        self.ax.grid(True, linestyle='--', alpha=0.7)
        self.ax.tick_params(axis='x', rotation=45)
        self.canvas.draw()

class BudgetManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Budget Manager")
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowIcon(QIcon('icon.ico'))

        self.current_lang = 'en'
        self.current_theme = 'Windows11'
        self.transactions = []
        self.categories = ['Food', 'Transportation', 'Utilities', 'Entertainment', 'Other']
        self.load_transactions()

        self.texts = {
            'en': {
                'title': 'Budget Manager',
                'add_transaction': 'Add Transaction',
                'amount_label': 'Amount:',
                'category_label': 'Category:',
                'type_label': 'Type:',
                'date_label': 'Date:',
                'description_label': 'Description:',
                'income': 'Income',
                'expense': 'Expense',
                'overview_tab': 'Overview',
                'transactions_tab': 'Transactions',
                'settings_tab': 'Settings',
                'clear_transactions': 'Clear Transactions',
                'save_transactions': 'Save Transactions to File',
                'status_idle': 'Managing your budget...',
                'status_added': 'Transaction added: {amount} at {time}',
                'status_cleared': 'All transactions cleared at {time}',
                'balance_label': 'Current Balance:',
                'income_label': 'Total Income:',
                'expense_label': 'Total Expenses:',
                'table_date': 'Date',
                'table_type': 'Type',
                'table_category': 'Category',
                'table_amount': 'Amount',
                'table_description': 'Description',
                'theme_label': 'Theme:',
                'language_label': 'Language:',
                'apply': 'Apply',
                'file_menu': 'File',
                'exit_action': 'Exit',
                'about': 'About',
                'about_text': 'Budget Manager\nVersion 1.0\nDeveloped by Hamid Yarali\nGitHub: https://github.com/HamidYaraliOfficial\nInstagram: https://www.instagram.com/hamidyaraliofficial\nTelegram: @Hamid_Yarali',
                'overview_title': 'Financial Overview',
                'add_button': 'Add',
                'delete_button': 'Delete Selected'
            },
            'fa': {
                'title': 'مدیریت بودجه',
                'add_transaction': 'افزودن تراکنش',
                'amount_label': 'مقدار:',
                'category_label': 'دسته‌بندی:',
                'type_label': 'نوع:',
                'date_label': 'تاریخ:',
                'description_label': 'توضیحات:',
                'income': 'درآمد',
                'expense': 'هزینه',
                'overview_tab': 'نمای کلی',
                'transactions_tab': 'تراکنش‌ها',
                'settings_tab': 'تنظیمات',
                'clear_transactions': 'پاک کردن تراکنش‌ها',
                'save_transactions': 'ذخیره تراکنش‌ها در فایل',
                'status_idle': 'مدیریت بودجه شما...',
                'status_added': 'تراکنش اضافه شد: {amount} در {time}',
                'status_cleared': 'همه تراکنش‌ها پاک شدند در {time}',
                'balance_label': 'تراز کنونی:',
                'income_label': 'کل درآمدها:',
                'expense_label': 'کل هزینه‌ها:',
                'table_date': 'تاریخ',
                'table_type': 'نوع',
                'table_category': 'دسته‌بندی',
                'table_amount': 'مقدار',
                'table_description': 'توضیحات',
                'theme_label': 'تم:',
                'language_label': 'زبان:',
                'apply': 'اعمال',
                'file_menu': 'فایل',
                'exit_action': 'خروج',
                'about': 'درباره',
                'about_text': 'مدیریت بودجه\nنسخه ۱.۰\nتوسعه‌یافته توسط حمید یارعلی\nگیت‌هاب: https://github.com/HamidYaraliOfficial\nاینستاگرام: https://www.instagram.com/hamidyaraliofficial\nتلگرام: @Hamid_Yarali',
                'overview_title': 'نمای کلی مالی',
                'add_button': 'افزودن',
                'delete_button': 'حذف انتخاب‌شده'
            },
            'zh': {
                'title': '预算管理器',
                'add_transaction': '添加交易',
                'amount_label': '金额：',
                'category_label': '类别：',
                'type_label': '类型：',
                'date_label': '日期：',
                'description_label': '描述：',
                'income': '收入',
                'expense': '支出',
                'overview_tab': '概览',
                'transactions_tab': '交易',
                'settings_tab': '设置',
                'clear_transactions': '清除交易',
                'save_transactions': '将交易保存到文件',
                'status_idle': '正在管理您的预算...',
                'status_added': '交易已添加：{amount} 在 {time}',
                'status_cleared': '所有交易已清除 在 {time}',
                'balance_label': '当前余额：',
                'income_label': '总收入：',
                'expense_label': '总 هزینه：',
                'table_date': '日期',
                'table_type': '类型',
                'table_category': '类别',
                'table_amount': '金额',
                'table_description': '描述',
                'theme_label': '主题：',
                'language_label': '语言：',
                'apply': '应用',
                'file_menu': '文件',
                'exit_action': '退出',
                'about': '关于',
                'about_text': '预算管理器\n版本 1.0\n由 Hamid Yarali 开发\nGitHub: https://github.com/HamidYaraliOfficial\nInstagram: https://www.instagram.com/hamidyaraliofficial\nTelegram: @Hamid_Yarali',
                'overview_title': '财务概览',
                'add_button': '添加',
                'delete_button': '删除所选'
            },
            'ru': {
                'title': 'Менеджер бюджета',
                'add_transaction': 'Добавить транзакцию',
                'amount_label': 'Сумма:',
                'category_label': 'Категория:',
                'type_label': 'Тип:',
                'date_label': 'Дата:',
                'description_label': 'Описание:',
                'income': 'Доход',
                'expense': 'Расход',
                'overview_tab': 'Обзор',
                'transactions_tab': 'Транзакции',
                'settings_tab': 'Настройки',
                'clear_transactions': 'Очистить транзакции',
                'save_transactions': 'Сохранить транзакции в файл',
                'status_idle': 'Управление вашим бюджетом...',
                'status_added': 'Транзакция добавлена: {amount} в {time}',
                'status_cleared': 'Все транзакции очищены в {time}',
                'balance_label': 'Текущий баланс:',
                'income_label': 'Общий доход:',
                'expense_label': 'Общие расходы:',
                'table_date': 'Дата',
                'table_type': 'Тип',
                'table_category': 'Категория',
                'table_amount': 'Сумма',
                'table_description': 'Описание',
                'theme_label': 'Тема:',
                'language_label': 'Язык:',
                'apply': 'Применить',
                'file_menu': 'Файл',
                'exit_action': 'Выход',
                'about': 'О программе',
                'about_text': 'Менеджер бюджета\nВерсия 1.0\nРазработано Hamid Yarali\nGitHub: https://github.com/HamidYaraliOfficial\nInstagram: https://www.instagram.com/hamidyaraliofficial\nTelegram: @Hamid_Yarali',
                'overview_title': 'Финансовый обзор',
                'add_button': 'Добавить',
                'delete_button': 'Удалить выбранное'
            }
        }

        self.themes = {
            'Windows11': {
                'background': QColor(243, 243, 243),
                'text': QColor(0, 0, 0),
                'button': QColor(225, 225, 225),
                'button_text': QColor(0, 0, 0),
                'button_hover': QColor(200, 200, 200),
                'accent': QColor(0, 90, 158),
                'border': QColor(180, 180, 180),
                'header': QColor(230, 230, 230),
                'progress': QColor(0, 90, 158),
                'warning': QColor(255, 204, 204)
            },
            'Dark': {
                'background': QColor(32, 32, 32),
                'text': QColor(230, 230, 230),
                'button': QColor(50, 50, 50),
                'button_text': QColor(230, 230, 230),
                'button_hover': QColor(70, 70, 70),
                'accent': QColor(0, 120, 212),
                'border': QColor(80, 80, 80),
                'header': QColor(40, 40, 40),
                'progress': QColor(0, 120, 212),
                'warning': QColor(100, 50, 50)
            },
            'Light': {
                'background': QColor(255, 255, 255),
                'text': QColor(0, 0, 0),
                'button': QColor(240, 240, 240),
                'button_text': QColor(0, 0, 0),
                'button_hover': QColor(220, 220, 220),
                'accent': QColor(0, 120, 212),
                'border': QColor(200, 200, 200),
                'header': QColor(245, 245, 245),
                'progress': QColor(0, 120, 212),
                'warning': QColor(255, 204, 204)
            },
            'Red': {
                'background': QColor(255, 235, 235),
                'text': QColor(80, 0, 0),
                'button': QColor(255, 200, 200),
                'button_text': QColor(80, 0, 0),
                'button_hover': QColor(255, 180, 180),
                'accent': QColor(200, 0, 0),
                'border': QColor(220, 150, 150),
                'header': QColor(255, 220, 220),
                'progress': QColor(200, 0, 0),
                'warning': QColor(255, 150, 150)
            },
            'Blue': {
                'background': QColor(235, 245, 255),
                'text': QColor(0, 0, 80),
                'button': QColor(200, 220, 255),
                'button_text': QColor(0, 0, 80),
                'button_hover': QColor(180, 200, 255),
                'accent': QColor(0, 0, 200),
                'border': QColor(150, 180, 220),
                'header': QColor(220, 235, 255),
                'progress': QColor(0, 0, 200),
                'warning': QColor(150, 200, 255)
            }
        }

        self.init_ui()
        self.apply_theme(self.current_theme)
        self.update_texts()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)

        self.menu_bar = QMenuBar()
        self.file_menu = QMenu(self.texts['en']['file_menu'])
        self.exit_action = self.file_menu.addAction(self.texts['en']['exit_action'])
        self.exit_action.triggered.connect(self.close)
        self.about_action = self.file_menu.addAction(self.texts['en']['about'])
        self.about_action.triggered.connect(self.show_about)
        self.menu_bar.addMenu(self.file_menu)
        self.main_layout.addWidget(self.menu_bar)

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                background: rgba(255, 255, 255, 0.95);
            }
            QTabBar::tab {
                padding: 10px 20px;
                margin-right: 5px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                background: rgba(0, 0, 0, 0.05);
                color: black;
            }
            QTabBar::tab:selected {
                background: rgba(0, 90, 158, 0.3);
                font-weight: bold;
                color: black;
            }
        """)
        self.main_layout.addWidget(self.tabs)

        self.overview_tab = QWidget()
        self.overview_layout = QVBoxLayout(self.overview_tab)
        self.overview_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.overview_layout.setSpacing(10)

        self.balance_label = QLabel()
        self.balance_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        self.income_label = QLabel()
        self.income_label.setFont(QFont("Segoe UI", 12))
        self.expense_label = QLabel()
        self.expense_label.setFont(QFont("Segoe UI", 12))
        self.graph = GraphWidget()
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setFixedHeight(100)
        self.status_text.setStyleSheet("""
            QTextEdit {
                border-radius: 8px;
                font-size: 14px;
                border: 1px solid rgba(0, 0, 0, 0.2);
                background: rgba(255, 255, 255, 0.95);
                color: black;
            }
        """)
        self.overview_layout.addWidget(self.balance_label)
        self.overview_layout.addWidget(self.income_label)
        self.overview_layout.addWidget(self.expense_label)
        self.overview_layout.addWidget(self.graph)
        self.overview_layout.addWidget(self.status_text)

        self.transactions_tab = QWidget()
        self.transactions_layout = QVBoxLayout(self.transactions_tab)
        self.transactions_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.transactions_layout.setSpacing(10)

        self.add_transaction_widget = QWidget()
        self.add_transaction_layout = QGridLayout(self.add_transaction_widget)
        self.add_transaction_layout.setSpacing(10)

        self.amount_label = QLabel()
        self.amount_label.setFont(QFont("Segoe UI", 12))
        self.amount_input = QLineEdit()
        self.amount_input.setFixedHeight(40)
        self.amount_input.setStyleSheet("""
            QLineEdit {
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                border: 1px solid rgba(0, 0, 0, 0.2);
                background: rgba(255, 255, 255, 0.95);
                color: black;
            }
        """)
        self.category_label = QLabel()
        self.category_label.setFont(QFont("Segoe UI", 12))
        self.category_combo = QComboBox()
        self.category_combo.addItems(self.categories)
        self.category_combo.setFixedHeight(40)
        self.category_combo.setStyleSheet("""
            QComboBox {
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                border: 1px solid rgba(0, 0, 0, 0.2);
                background: rgba(255, 255, 255, 0.95);
                color: black;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)
        self.type_label = QLabel()
        self.type_label.setFont(QFont("Segoe UI", 12))
        self.type_combo = QComboBox()
        self.type_combo.addItems([self.texts['en']['income'], self.texts['en']['expense']])
        self.type_combo.setFixedHeight(40)
        self.type_combo.setStyleSheet("""
            QComboBox {
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                border: 1px solid rgba(0, 0, 0, 0.2);
                background: rgba(255, 255, 255, 0.95);
                color: black;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)
        self.date_label = QLabel()
        self.date_label.setFont(QFont("Segoe UI", 12))
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setFixedHeight(40)
        self.date_input.setStyleSheet("""
            QDateEdit {
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                border: 1px solid rgba(0, 0, 0, 0.2);
                background: rgba(255, 255, 255, 0.95);
                color: black;
            }
        """)
        self.description_label = QLabel()
        self.description_label.setFont(QFont("Segoe UI", 12))
        self.description_input = QLineEdit()
        self.description_input.setFixedHeight(40)
        self.description_input.setStyleSheet("""
            QLineEdit {
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                border: 1px solid rgba(0, 0, 0, 0.2);
                background: rgba(255, 255, 255, 0.95);
                color: black;
            }
        """)
        self.add_button = QPushButton()
        self.add_button.setFixedHeight(40)
        self.add_button.setFont(QFont("Segoe UI", 12))
        self.add_button.setStyleSheet("""
            QPushButton {
                border-radius: 8px;
                font-size: 14px;
                border: 1px solid rgba(0, 0, 0, 0.1);
                background: rgba(0, 90, 158, 0.8);
                color: white;
            }
            QPushButton:hover {
                background: rgba(0, 90, 158, 1.0);
            }
        """)
        self.add_button.clicked.connect(self.add_transaction)

        self.add_transaction_layout.addWidget(self.amount_label, 0, 0)
        self.add_transaction_layout.addWidget(self.amount_input, 0, 1)
        self.add_transaction_layout.addWidget(self.category_label, 1, 0)
        self.add_transaction_layout.addWidget(self.category_combo, 1, 1)
        self.add_transaction_layout.addWidget(self.type_label, 2, 0)
        self.add_transaction_layout.addWidget(self.type_combo, 2, 1)
        self.add_transaction_layout.addWidget(self.date_label, 3, 0)
        self.add_transaction_layout.addWidget(self.date_input, 3, 1)
        self.add_transaction_layout.addWidget(self.description_label, 4, 0)
        self.add_transaction_layout.addWidget(self.description_input, 4, 1)
        self.add_transaction_layout.addWidget(self.add_button, 5, 0, 1, 2)

        self.transactions_table = QTableWidget()
        self.transactions_table.setColumnCount(5)
        self.transactions_table.setHorizontalHeaderLabels([
            self.texts['en']['table_date'],
            self.texts['en']['table_type'],
            self.texts['en']['table_category'],
            self.texts['en']['table_amount'],
            self.texts['en']['table_description']
        ])
        self.transactions_table.setStyleSheet("""
            QTableWidget {
                border-radius: 8px;
                font-size: 14px;
                border: 1px solid rgba(0, 0, 0, 0.2);
                background: rgba(255, 255, 255, 0.95);
                color: black;
            }
            QHeaderView::section {
                background: rgba(0, 90, 158, 0.1);
                padding: 5px;
                font-size: 14px;
                border: 1px solid rgba(0, 0, 0, 0.1);
                color: black;
            }
        """)
        self.transactions_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.transactions_table.setSelectionMode(QTableWidget.SelectionMode.MultiSelection)

        self.delete_button = QPushButton()
        self.delete_button.setFixedHeight(40)
        self.delete_button.setFont(QFont("Segoe UI", 12))
        self.delete_button.setStyleSheet("""
            QPushButton {
                border-radius: 8px;
                font-size: 14px;
                border: 1px solid rgba(0, 0, 0, 0.1);
                background: rgba(200, 0, 0, 0.8);
                color: white;
            }
            QPushButton:hover {
                background: rgba(200, 0, 0, 1.0);
            }
        """)
        self.delete_button.clicked.connect(self.delete_selected_transactions)

        self.clear_transactions_btn = QPushButton()
        self.clear_transactions_btn.setFixedHeight(40)
        self.clear_transactions_btn.setFont(QFont("Segoe UI", 12))
        self.clear_transactions_btn.setStyleSheet("""
            QPushButton {
                border-radius: 8px;
                font-size: 14px;
                border: 1px solid rgba(0, 0, 0, 0.1);
                background: rgba(200, 0, 0, 0.8);
                color: white;
            }
            QPushButton:hover {
                background: rgba(200, 0, 0, 1.0);
            }
        """)
        self.clear_transactions_btn.clicked.connect(self.clear_transactions)

        self.save_transactions_btn = QPushButton()
        self.save_transactions_btn.setFixedHeight(40)
        self.save_transactions_btn.setFont(QFont("Segoe UI", 12))
        self.save_transactions_btn.setStyleSheet("""
            QPushButton {
                border-radius: 8px;
                font-size: 14px;
                border: 1px solid rgba(0, 0, 0, 0.1);
                background: rgba(0, 90, 158, 0.8);
                color: white;
            }
            QPushButton:hover {
                background: rgba(0, 90, 158, 1.0);
            }
        """)
        self.save_transactions_btn.clicked.connect(self.save_transactions_to_file)

        self.transactions_layout.addWidget(self.add_transaction_widget)
        self.transactions_layout.addWidget(self.transactions_table)
        self.transactions_layout.addWidget(self.delete_button)
        self.transactions_layout.addWidget(self.clear_transactions_btn)
        self.transactions_layout.addWidget(self.save_transactions_btn)

        self.settings_tab = QWidget()
        self.settings_layout = QVBoxLayout(self.settings_tab)
        self.settings_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.settings_layout.setSpacing(10)

        self.language_label = QLabel()
        self.language_label.setFont(QFont("Segoe UI", 12))
        self.language_combo = QComboBox()
        self.language_combo.addItems(['English', 'فارسی', '中文', 'Русский'])
        self.language_combo.setFixedHeight(40)
        self.language_combo.setStyleSheet("""
            QComboBox {
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                border: 1px solid rgba(0, 0, 0, 0.2);
                background: rgba(255, 255, 255, 0.95);
                color: black;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)
        self.language_combo.currentIndexChanged.connect(self.change_language)

        self.theme_label = QLabel()
        self.theme_label.setFont(QFont("Segoe UI", 12))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(['Windows11', 'Dark', 'Light', 'Red', 'Blue'])
        self.theme_combo.setFixedHeight(40)
        self.theme_combo.setStyleSheet("""
            QComboBox {
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                border: 1px solid rgba(0, 0, 0, 0.2);
                background: rgba(255, 255, 255, 0.95);
                color: black;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)
        self.theme_combo.currentIndexChanged.connect(self.change_theme)

        self.apply_btn = QPushButton()
        self.apply_btn.setFixedHeight(40)
        self.apply_btn.setFont(QFont("Segoe UI", 12))
        self.apply_btn.setStyleSheet("""
            QPushButton {
                border-radius: 8px;
                font-size: 14px;
                border: 1px solid rgba(0, 0, 0, 0.1);
                background: rgba(0, 90, 158, 0.8);
                color: white;
            }
            QPushButton:hover {
                background: rgba(0, 90, 158, 1.0);
            }
        """)
        self.apply_btn.clicked.connect(self.apply_settings)

        self.settings_layout.addWidget(self.language_label)
        self.settings_layout.addWidget(self.language_combo)
        self.settings_layout.addWidget(self.theme_label)
        self.settings_layout.addWidget(self.theme_combo)
        self.settings_layout.addWidget(self.apply_btn)
        self.settings_layout.addStretch()

        self.tabs.addTab(self.overview_tab, self.texts['en']['overview_tab'])
        self.tabs.addTab(self.transactions_tab, self.texts['en']['transactions_tab'])
        self.tabs.addTab(self.settings_tab, self.texts['en']['settings_tab'])

        self.update_transactions_table()
        self.update_overview()

    def apply_theme(self, theme_name):
        palette = QPalette()
        theme = self.themes.get(theme_name, self.themes['Windows11'])
        palette.setColor(QPalette.ColorRole.Window, theme['background'])
        palette.setColor(QPalette.ColorRole.WindowText, theme['text'])
        palette.setColor(QPalette.ColorRole.Button, theme['button'])
        palette.setColor(QPalette.ColorRole.ButtonText, theme['button_text'])
        palette.setColor(QPalette.ColorRole.Highlight, theme['accent'])
        palette.setColor(QPalette.ColorRole.Base, theme['background'])
        palette.setColor(QPalette.ColorRole.AlternateBase, theme['header'])
        palette.setColor(QPalette.ColorRole.Text, theme['text'])
        self.setPalette(palette)
        self.setStyle(QStyleFactory.create('WindowsVista' if theme_name == 'Windows11' else 'Fusion'))
        self.status_text.setStyleSheet(f"""
            QTextEdit {{
                border-radius: 8px;
                font-size: 14px;
                border: 1px solid {theme['border'].name()};
                background: {theme['background'].name()};
                color: {theme['text'].name()};
            }}
        """)
        self.amount_input.setStyleSheet(f"""
            QLineEdit {{
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                border: 1px solid {theme['border'].name()};
                background: {theme['background'].name()};
                color: {theme['text'].name()};
            }}
        """)
        self.description_input.setStyleSheet(f"""
            QLineEdit {{
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                border: 1px solid {theme['border'].name()};
                background: {theme['background'].name()};
                color: {theme['text'].name()};
            }}
        """)
        self.category_combo.setStyleSheet(f"""
            QComboBox {{
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                border: 1px solid {theme['border'].name()};
                background: {theme['background'].name()};
                color: {theme['text'].name()};
            }}
            QComboBox::drop-down {{
                border: none;
            }}
        """)
        self.type_combo.setStyleSheet(f"""
            QComboBox {{
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                border: 1px solid {theme['border'].name()};
                background: {theme['background'].name()};
                color: {theme['text'].name()};
            }}
            QComboBox::drop-down {{
                border: none;
            }}
        """)
        self.date_input.setStyleSheet(f"""
            QDateEdit {{
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                border: 1px solid {theme['border'].name()};
                background: {theme['background'].name()};
                color: {theme['text'].name()};
            }}
        """)
        self.transactions_table.setStyleSheet(f"""
            QTableWidget {{
                border-radius: 8px;
                font-size: 14px;
                border: 1px solid {theme['border'].name()};
                background: {theme['background'].name()};
                color: {theme['text'].name()};
            }}
            QHeaderView::section {{
                background: {theme['header'].name()};
                padding: 5px;
                font-size: 14px;
                border: 1px solid {theme['border'].name()};
                color: {theme['text'].name()};
            }}
        """)

    def update_texts(self):
        lang = self.current_lang
        self.setWindowTitle(self.texts[lang]['title'])
        self.amount_label.setText(self.texts[lang]['amount_label'])
        self.category_label.setText(self.texts[lang]['category_label'])
        self.type_label.setText(self.texts[lang]['type_label'])
        self.date_label.setText(self.texts[lang]['date_label'])
        self.description_label.setText(self.texts[lang]['description_label'])
        self.add_button.setText(self.texts[lang]['add_button'])
        self.delete_button.setText(self.texts[lang]['delete_button'])
        self.clear_transactions_btn.setText(self.texts[lang]['clear_transactions'])
        self.save_transactions_btn.setText(self.texts[lang]['save_transactions'])
        self.balance_label.setText(self.texts[lang]['balance_label'])
        self.income_label.setText(self.texts[lang]['income_label'])
        self.expense_label.setText(self.texts[lang]['expense_label'])
        self.theme_label.setText(self.texts[lang]['theme_label'])
        self.language_label.setText(self.texts[lang]['language_label'])
        self.apply_btn.setText(self.texts[lang]['apply'])
        self.file_menu.setTitle(self.texts[lang]['file_menu'])
        self.exit_action.setText(self.texts[lang]['exit_action'])
        self.about_action.setText(self.texts[lang]['about'])
        self.status_text.setText(self.texts[lang]['status_idle'])

        self.tabs.setTabText(0, self.texts[lang]['overview_tab'])
        self.tabs.setTabText(1, self.texts[lang]['transactions_tab'])
        self.tabs.setTabText(2, self.texts[lang]['settings_tab'])

        self.transactions_table.setHorizontalHeaderLabels([
            self.texts[lang]['table_date'],
            self.texts[lang]['table_type'],
            self.texts[lang]['table_category'],
            self.texts[lang]['table_amount'],
            self.texts[lang]['table_description']
        ])

        alignment = Qt.AlignmentFlag.AlignRight if lang == 'fa' else Qt.AlignmentFlag.AlignLeft
        self.amount_label.setAlignment(alignment)
        self.category_label.setAlignment(alignment)
        self.type_label.setAlignment(alignment)
        self.date_label.setAlignment(alignment)
        self.description_label.setAlignment(alignment)
        self.balance_label.setAlignment(alignment)
        self.income_label.setAlignment(alignment)
        self.expense_label.setAlignment(alignment)
        self.theme_label.setAlignment(alignment)
        self.language_label.setAlignment(alignment)
        self.status_text.setAlignment(alignment)

        self.update_transactions_table()
        self.update_overview()

    def change_language(self, index):
        langs = ['en', 'fa', 'zh', 'ru']
        self.current_lang = langs[index]
        self.type_combo.clear()
        self.type_combo.addItems([self.texts[self.current_lang]['income'], self.texts[self.current_lang]['expense']])
        self.update_texts()

    def change_theme(self, index):
        themes = ['Windows11', 'Dark', 'Light', 'Red', 'Blue']
        self.current_theme = themes[index]
        self.apply_theme(self.current_theme)

    def apply_settings(self):
        self.update_texts()
        self.apply_theme(self.current_theme)

    def show_about(self):
        QMessageBox.information(self, self.texts[self.current_lang]['about'], 
                               self.texts[self.current_lang]['about_text'])

    def add_transaction(self):
        try:
            amount = float(self.amount_input.text())
            category = self.category_combo.currentText()
            type_ = self.type_combo.currentText()
            date = self.date_input.date().toString("yyyy-MM-dd")
            description = self.description_input.text()

            if type_ == self.texts[self.current_lang]['income']:
                type_key = 'income'
            else:
                type_key = 'expense'

            transaction = {
                'amount': amount,
                'category': category,
                'type': type_key,
                'date': date,
                'description': description,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.transactions.append(transaction)
            self.save_transactions()
            self.update_transactions_table()
            self.update_overview()
            self.status_text.setText(self.texts[self.current_lang]['status_added'].format(
                amount=amount, time=transaction['timestamp']))
            self.clear_inputs()
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid amount.")

    def delete_selected_transactions(self):
        selected_rows = sorted(set(index.row() for index in self.transactions_table.selectedIndexes()), reverse=True)
        for row in selected_rows:
            if 0 <= row < len(self.transactions):
                self.transactions.pop(row)
        self.save_transactions()
        self.update_transactions_table()
        self.update_overview()
        self.status_text.setText(self.texts[self.current_lang]['status_cleared'].format(
            time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def clear_transactions(self):
        self.transactions = []
        self.save_transactions()
        self.update_transactions_table()
        self.update_overview()
        self.status_text.setText(self.texts[self.current_lang]['status_cleared'].format(
            time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def save_transactions(self):
        with open('budget_transactions.json', 'w', encoding='utf-8') as f:
            json.dump(self.transactions, f, ensure_ascii=False, indent=4)

    def load_transactions(self):
        try:
            with open('budget_transactions.json', 'r', encoding='utf-8') as f:
                self.transactions = json.load(f)
        except FileNotFoundError:
            self.transactions = []

    def save_transactions_to_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, self.texts[self.current_lang]['save_transactions'], "", "JSON Files (*.json)")
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.transactions, f, ensure_ascii=False, indent=4)
            self.status_text.setText(self.texts[self.current_lang]['status_added'].format(
                amount="Transactions", time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def update_transactions_table(self):
        self.transactions_table.setRowCount(len(self.transactions))
        for row, transaction in enumerate(self.transactions):
            self.transactions_table.setItem(row, 0, QTableWidgetItem(transaction['date']))
            type_text = self.texts[self.current_lang]['income'] if transaction['type'] == 'income' else self.texts[self.current_lang]['expense']
            self.transactions_table.setItem(row, 1, QTableWidgetItem(type_text))
            self.transactions_table.setItem(row, 2, QTableWidgetItem(transaction['category']))
            self.transactions_table.setItem(row, 3, QTableWidgetItem(f"{transaction['amount']:.2f}"))
            self.transactions_table.setItem(row, 4, QTableWidgetItem(transaction['description']))
            for col in range(5):
                self.transactions_table.item(row, col).setTextAlignment(
                    Qt.AlignmentFlag.AlignRight if self.current_lang == 'fa' else Qt.AlignmentFlag.AlignLeft)

    def update_overview(self):
        total_income = sum(t['amount'] for t in self.transactions if t['type'] == 'income')
        total_expense = sum(t['amount'] for t in self.transactions if t['type'] == 'expense')
        balance = total_income - total_expense

        self.balance_label.setText(f"{self.texts[self.current_lang]['balance_label']} {balance:.2f}")
        self.income_label.setText(f"{self.texts[self.current_lang]['income_label']} {total_income:.2f}")
        self.expense_label.setText(f"{self.texts[self.current_lang]['expense_label']} {total_expense:.2f}")

        categories = self.categories
        amounts = [sum(t['amount'] for t in self.transactions if t['category'] == cat and t['type'] == 'expense') for cat in categories]
        self.graph.update_graph(categories, amounts, self.texts[self.current_lang]['overview_title'], self.current_lang)

    def clear_inputs(self):
        self.amount_input.clear()
        self.category_combo.setCurrentIndex(0)
        self.type_combo.setCurrentIndex(0)
        self.date_input.setDate(QDate.currentDate())
        self.description_input.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Windows')
    window = BudgetManagerApp()
    window.show()
    sys.exit(app.exec())