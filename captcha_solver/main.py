from src.captcha_solver import CaptchaSolver
from src.automation import solve_captcha_automatically


def main():
    solver = CaptchaSolver()
    solve_captcha_automatically("https://example.com/captcha", solver)

if __name__ == "__main__":
    main()
