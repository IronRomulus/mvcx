import { Form } from "@/components/form/form";
import { Link } from "@/components/form/link";
import { ThemeController } from "@/components/theme-controller/theme-controller";

type Component = {
  element: CustomElementConstructor;
  options?: ElementDefinitionOptions;
};

export const COMPONENTS: Record<string, Component> = {
  "c-form": {
    element: Form,
    options: { extends: "form" },
  },
  "c-link": {
    element: Link,
    options: { extends: "a" },
  },
  "c-theme-controller": {
    element: ThemeController,
    options: { extends: "button" },
  },
};
