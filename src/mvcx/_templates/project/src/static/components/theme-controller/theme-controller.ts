import { appObserver } from "@/observers";
import { appState, type Theme } from "@/state";
import { createElement, Moon, Sun } from "lucide";

export class ThemeController extends HTMLButtonElement {
  constructor() {
    super();

    this._handleClick = this._handleClick.bind(this);
    this._handleThemeChange = this._handleThemeChange.bind(this);
  }

  connectedCallback(): void {
    this.addEventListener("click", this._handleClick);
    appObserver.attach("theme-change", this._handleThemeChange);
  }

  disconnectedCallback(): void {
    this.removeEventListener("click", this._handleClick);
    appObserver.detach("theme-change", this._handleThemeChange);
  }

  private _handleClick(): void {
    appState.theme = appState.theme === "light" ? "dark" : "light";
    appObserver.notify("theme-change", appState.theme);
  }

  private _handleThemeChange(newTheme: Theme): void {
    this.innerHTML = "";
    const newIcon = createElement(newTheme === "light" ? Sun : Moon);
    this.appendChild(newIcon);
  }
}
