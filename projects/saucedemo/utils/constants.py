

class Urls:
    BASE: str = "https://www.saucedemo.com"

    LOGIN: str = f"{BASE}/"
    INVENTORY: str = f"{BASE}/inventory.html"
    CART: str = f"{BASE}/cart.html"
    CHECKOUT: str = f"{BASE}/checkout-step-one.html"


class Users:
    standard_user_username: str = "standard_user"
    locked_out_user_username: str = "locked_out_user"
    problem_user_username: str = "problem_user"
    performance_glitch_user_username: str = "performance_glitch_user"
    error_user_username: str = "error_user"
    visual_user_username: str = "visual_user"

    password: str = "secret_sauce"
