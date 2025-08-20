import { navigateTo } from "@/utils";

export class Link extends HTMLAnchorElement {
  constructor() {
    super();

    this._handleClick = this._handleClick.bind(this);
  }

  connectedCallback(): void {
    this.addEventListener("click", this._handleClick);
  }

  disconnectedCallback(): void {
    this.removeEventListener("click", this._handleClick);
  }

  private async _handleClick(event: MouseEvent): Promise<void> {
    event.preventDefault();
    await navigateTo(this.href);
  }
}
