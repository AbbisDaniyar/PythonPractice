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


class ColorGameBot:
    """Оптимизированный бот для цветовой игры"""

    def __init__(self, headless=False):
        self.setup_driver(headless)
        self.score = 0
        self.start_time = 0

    def setup_driver(self, headless):
        """Настройка Chrome драйвера с оптимизацией"""
        chrome_options = Options()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        if headless:
            chrome_options.add_argument("--headless")

        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service, options=chrome_options)
        self.driver.set_window_size(1200, 800)

    def start_game(self):
        """Быстрый запуск игры"""
        print("🚀 Запуск оптимизированного бота...")
        self.driver.get("https://www.arealme.com/colors/ru/")
        time.sleep(1.5)

        start_btn = self.driver.find_element(By.ID, "start")
        start_btn.click()
        print("🎮 Игра начата!")
        self.start_time = time.time()
        time.sleep(2.0)
        return True

    def get_remaining_time(self):
        """Получение оставшегося времени"""
        elapsed = time.time() - self.start_time
        return max(0, 60 - elapsed)

    def play_round_fast(self):
        """Оптимизированный раунд с использованием JavaScript"""
        script = """
        var container = document.querySelector('.patra-color');
        if (!container) return false;
        
        var spans = container.querySelectorAll('span');
        var colorMap = {};
        var elements = [];
        
        for (var i = 0; i < spans.length; i++) {
            var span = spans[i];
            var style = window.getComputedStyle(span);
            var bgColor = style.backgroundColor;
            
            if (bgColor && bgColor.startsWith('rgb') && 
                bgColor !== 'rgba(0, 0, 0, 0)' && 
                span.offsetWidth > 0) {
                
                elements.push(span);
                
                if (!colorMap[bgColor]) {
                    colorMap[bgColor] = [];
                }
                colorMap[bgColor].push(span);
            }
        }
        
        // Находим уникальный цвет
        for (var color in colorMap) {
            if (colorMap[color].length === 1) {
                colorMap[color][0].click();
                return true;
            }
        }
        
        return false;
        """

        try:
            result = self.driver.execute_script(script)
            if result:
                self.score += 1
                return True
        except:
            pass

        return False

    def run_game(self):
        """Основной игровой цикл с мониторингом"""
        if not self.start_game():
            return

        print("⏱ Игра началась! Время: 60 секунд")
        last_print_time = self.start_time

        # Оптимизированный игровой цикл
        while self.get_remaining_time() > 0:
            self.play_round_fast()

            # Вывод прогресса каждые 5 секунд
            current_time = time.time()
            if current_time - last_print_time >= 5:
                remaining = self.get_remaining_time()
                speed = self.score / (current_time - self.start_time)
                print(f"⚡ Счет: {self.score} | Скорость: {speed:.1f} клик/сек | Осталось: {remaining:.1f} сек")
                last_print_time = current_time

        final_time = time.time() - self.start_time
        final_speed = self.score / final_time

        print(f"\n🎯 ФИНАЛЬНЫЙ РЕЗУЛЬТАТ: {self.score} очков")
        print(f"📊 Средняя скорость: {final_speed:.1f} кликов/сек")

        self.driver.save_screenshot(f"optimized_result_{self.score}.png")

    def close(self):
        """Закрытие браузера"""
        self.driver.quit()


def main():
    print("=" * 50)
    print("          🎯 ОПТИМИЗИРОВАННЫЙ БОТ")
    print("=" * 50)

    # Запуск в headless режиме для максимальной производительности
    bot = ColorGameBot(headless=True)
    try:
        bot.run_game()

        if bot.score >= 1669:
            print("🎉 РЕКОРД ПРЕВЫШЕН!")
        else:
            print("💪 Хорошая попытка!")

    finally:
        bot.close()


if __name__ == "__main__":
    main()