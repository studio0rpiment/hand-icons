import type { SVGProps } from "react";
import type { IconDirection, IconName, IconVariant } from "./icons";

export interface IconProps extends Omit<SVGProps<SVGSVGElement>, "name"> {
  name: IconName;
  /** "line" = hollow trace of the ink, "fill" = solid (closed shapes filled). Default "line". */
  variant?: IconVariant;
  /** rotation / mirror sibling; "base" is as drawn. Default "base". */
  direction?: IconDirection;
  /** size in rem (sets font-size; the icon is 1em square). Default 1.5. */
  size?: number;
  /** accessible label; omitted = decorative (aria-hidden) */
  label?: string;
  /** path to the sprite file when it isn't inlined in the document, e.g. "/assets/hand-icons.svg" */
  sprite?: string;
}

/** Hand-drawn icon rendered from the sprite. Colour follows CSS `color`. */
export function Icon({ name, variant = "line", direction = "base", size = 1.5, label, sprite = "", className, style, ...rest }: IconProps) {
  const id = `hi-${name}-${variant}${direction === "base" ? "" : `-${direction}`}`;
  return (
    <svg
      className={["hi", className].filter(Boolean).join(" ")}
      style={{ fontSize: `${size}rem`, ...style }}
      role={label ? "img" : undefined}
      aria-label={label}
      aria-hidden={label ? undefined : true}
      {...rest}
    >
      <use href={`${sprite}#${id}`} />
    </svg>
  );
}
