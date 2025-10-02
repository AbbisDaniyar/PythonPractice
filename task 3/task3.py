"""
Color Game Bot - автоматизация игры на определение цветов
Рекордная версия с показателем 3171 очков
https://www.arealme.com/colors/ru/
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


class ExtremeColorBot:
    """
    Экстремально оптимизированный бот для установки рекордов
    Достигнутый результат: 3171 очков за 60 секунд
    """

    def __init__(self):
        self.setup_driver()
        self.score = 0

    def setup_driver(self):
        """Максимальная оптимизация Chrome драйвера"""
        chrome_options = Options()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--headless")  # Ключевой параметр для скорости

        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service, options=chrome_options)
        self.driver.set_window_size(1200, 800)

    def start_game(self):
        """Сверхбыстрый запуск игры"""
        print("🚀 Запуск рекордного бота...")
        self.driver.get("https://www.arealme.com/colors/ru/")
        time.sleep(1.0)

        start_btn = self.driver.find_element(By.ID, "start")
        start_btn.click()
        time.sleep(2.0)
        return True

    def run_game(self):
        """Основной игровой цикл с максимальной производительностью"""
        if not self.start_game():
            return

        print("🎮 Игра началась! Цель: 1669+ очков")
        start_time = time.time()
        end_time = start_time + 60
        last_print_time = start_time

        # Экстремально оптимизированный цикл
        while time.time() < end_time:
            try:
                # Ультра-быстрый JavaScript для поиска и клика
                script = """
                var c = document.querySelector('.patra-color');
                if (!c) return false;
                var s = c.querySelectorAll('span'), m = {}, e = [];
                for (var i = 0; i < s.length; i++) {
                    var sp = s[i], st = window.getComputedStyle(sp), bg = st.backgroundColor;
                    if (bg && bg.startsWith('rgb') && bg !== 'rgba(0,0,0,0)' && sp.offsetWidth > 0) {
                        e.push(sp);
                        m[bg] ? m[bg].push(sp) : m[bg] = [sp];
                    }
                }
                for (var clr in m) if (m[clr].length === 1) { m[clr][0].click(); return true; }
                return false;
                """

                result = self.driver.execute_script(script)
                if result:
                    self.score += 1

                # Прогресс каждые 3 секунды
                current_time = time.time()
                if current_time - last_print_time >= 3:
                    remaining = end_time - current_time
                    speed = self.score / (current_time - start_time)
                    print(f"⚡ Счет: {self.score} | Скорость: {speed:.1f} клик/сек | Осталось: {remaining:.1f} сек")
                    last_print_time = current_time

            except Exception:
                # Продолжаем при любых ошибках
                continue

        # Финальные результаты
        total_time = time.time() - start_time
        final_speed = self.score / total_time

        print(f"\n🎯 ФИНАЛЬНЫЙ РЕЗУЛЬТАТ: {self.score} очков")
        print(f"📊 Средняя скорость: {final_speed:.1f} кликов/сек")
        print(f"⏰ Общее время: {total_time:.1f} секунд")

        # Сохраняем скриншот
        self.driver.save_screenshot(f"record_{self.score}.png")

        # Анализ достижения
        if self.score >= 1669:
            print("🏆🎉 РЕКОРД 1669+ ПРЕВЫШЕН! 🎉🏆")
        else:
            print("💪 Хорошая попытка!")

    def close(self):
        """Закрытие браузера"""
        self.driver.quit()


def main():
    print("=" * 60)
    print("          🎯 БОТ ДЛЯ ЦВЕТОВОЙ ИГРЫ")
    print("          Рекордная версия: 3171 очков")
    print("=" * 60)

    bot = ExtremeColorBot()
    try:
        bot.run_game()

        print("\n" + "=" * 50)
        if bot.score >= 1669:
            print(f"🎉 ПОЗДРАВЛЯЕМ! РЕКОРД: {bot.score} очков!")
        else:
            print(f"✅ Результат: {bot.score} очков")
        print("=" * 50)

    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        bot.close()


if __name__ == "__main__":
    main()