export function parseHtml(text: string): Document {
  const parser = new DOMParser();
  return parser.parseFromString(text, "text/html");
}

export async function navigateTo(path: string): Promise<void> {
  const response = await fetch(path);

  const newDocument = parseHtml(await response.text());
  const newBody = newDocument.querySelector("body")!;

  document.querySelector("body")!.innerHTML = newBody.innerHTML;

  history.pushState({ url: response.url }, "", response.url);
}
