import { getCookie } from "typescript-cookie";

export class Form extends HTMLFormElement {
  constructor() {
    super();

    this._handleSubmit = this._handleSubmit.bind(this);
  }

  connectedCallback(): void {
    this.addEventListener("submit", this._handleSubmit);
  }

  disconnectedCallback(): void {
    this.removeEventListener("submit", this._handleSubmit);
  }

  private async _handleSubmit(event: SubmitEvent): Promise<void> {
    event.preventDefault();

    const formData = new FormData(this);

    this.setAttribute("disabled", "");

    const response = await fetch(this.action, {
      method: this.method,
      headers: {
        "x-csrftoken": getCookie("csrftoken") as string,
      },
      body: formData,
    });

    response.ok
      ? await this._handleSuccess(response)
      : await this._handleFailure(response);
  }

  private async _handleSuccess(response: Response): Promise<void> {}

  private async _handleFailure(response: Response): Promise<void> {}
}
