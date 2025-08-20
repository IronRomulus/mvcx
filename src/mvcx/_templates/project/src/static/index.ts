import { COMPONENTS } from "@/registry";
import { parseHtml } from "@/utils";

function init(): void {
  window.addEventListener(
    "popstate",
    async function (event: PopStateEvent): Promise<void> {
      const url: string = event.state.url ?? this.location.href;
      const response = await this.fetch(url);
      const newDocument = parseHtml(await response.text());
      const newBody = newDocument.querySelector("body")!;
      this.document.querySelector("body")!.innerHTML = newBody.innerHTML;
    },
  );

  for (const componentName in COMPONENTS) {
    const component = COMPONENTS[componentName]!;
    customElements.define(componentName, component.element, component.options);
  }
}

init();
