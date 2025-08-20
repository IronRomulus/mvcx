import { getCookie, setCookie } from "typescript-cookie";

export type Theme = "light" | "dark";

class AppState {
  private _theme: Theme = (getCookie("theme") as Theme | undefined) ?? "light";

  get theme(): Theme {
    return this._theme;
  }

  set theme(newTheme: Theme) {
    this._theme = newTheme;
    setCookie("theme", newTheme);
    document.documentElement.dataset.theme = newTheme;
  }
}

export const appState = new AppState();
