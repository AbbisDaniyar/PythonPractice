"""
Color Game Bot - автоматизация игры на определение цветов
https://www.arealme.com/colors/ru/
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from collections import Counter


class ColorGameBot:
    """Основной класс бота для цветовой игры"""

    def __init__(self):
        self.setup_driver()
        self.score = 0
        self.start_time = 0

    def setup_driver(self):
        """Настройка Chrome драйвера"""
        chrome_options = Options()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")

        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service, options=chrome_options)
        self.driver.set_window_size(1200, 800)

    def start_game(self):
        """Запуск игры"""
        print("Запуск бота...")
        self.driver.get("https://www.arealme.com/colors/ru/")
        time.sleep(2)

        start_btn = self.driver.find_element(By.ID, "start")
        start_btn.click()
        print("🎮 Игра начата!")
        self.start_time = time.time()
        time.sleep(2)

    def get_remaining_time(self):
        """Получение оставшегося времени"""
        elapsed = time.time() - self.start_time
        return max(0, 60 - elapsed)

    def find_color_elements(self):
        """Поиск цветных элементов на странице"""
        try:
            container = self.driver.find_element(By.CSS_SELECTOR, ".patra-color")
            spans = container.find_elements(By.TAG_NAME, "span")

            color_elements = []
            for span in spans:
                try:
                    bg_color = span.value_of_css_property('background-color')
                    if bg_color and bg_color.startswith('rgb'):
                        color_elements.append(span)
                except:
                    continue

            return color_elements
        except:
            return []

    def find_unique_color(self, elements):
        """Поиск уникального цвета среди элементов"""
        if len(elements) < 4:
            return None

        colors = []
        for element in elements:
            try:
                color = element.value_of_css_property('background-color')
                colors.append(color)
            except:
                continue

        color_count = Counter(colors)
        for color, count in color_count.items():
            if count == 1:
                for element in elements:
                    if element.value_of_css_property('background-color') == color:
                        return element

        return None

    def play_round(self):
        """Выполнение одного раунда игры"""
        elements = self.find_color_elements()
        if not elements:
            return False

        unique_element = self.find_unique_color(elements)
        if unique_element:
            try:
                unique_element.click()
                self.score += 1
                return True
            except:
                return False

        return False

    def run_game(self):
        """Основной игровой цикл"""
        if not self.start_game():
            return

        print("⏱ Игра началась! Время: 60 секунд")

        # Основной игровой цикл
        while self.get_remaining_time() > 0:
            self.play_round()
            time.sleep(0.1)

        print(f"Финальный счет: {self.score}")
        self.driver.save_screenshot(f"result_{self.score}.png")

    def close(self):
        """Закрытие браузера"""
        self.driver.quit()


def main():
    bot = ColorGameBot()
    try:
        bot.run_game()
    finally:
        bot.close()


if __name__ == "__main__":
    main()