import { Layout, Code, Palette, Layers } from "lucide-react";

const features = [
  {
    name: "AI-Generated Layouts",
    description: "Automatically generate stunning and responsive website layouts with AI.",
    icon: Layout,
  },
  {
    name: "No-Code Customization",
    description: "Easily customize your site without writing a single line of code.",
    icon: Code,
  },
  {
    name: "Smart Design Assistant",
    description: "AI suggests colors, fonts, and layouts that best match your brand identity.",
    icon: Palette,
  },
  {
    name: "Custom Styled Websites",
    description: "Get beautifully designed websites with Bootstrap for a polished, professional look.",
    icon: Layers,
  },
];

export default function Features() {
  return (
    <section className="container space-y-16 py-24 md:py-32">
      <div className="mx-auto max-w-[58rem] text-center">
        <h2 className="font-bold text-3xl leading-[1.1] sm:text-3xl md:text-5xl">
          AI-Powered Website Generator
        </h2>
        <p className="mt-4 text-muted-foreground sm:text-lg">
          Effortlessly create stunning websites with the power of AI—no coding required.
        </p>
      </div>
      <div className="mx-auto grid max-w-5xl grid-cols-1 gap-8 md:grid-cols-2">
        {features.map((feature) => (
          <div key={feature.name} className="relative overflow-hidden rounded-lg border bg-background p-8">
            <div className="flex items-center gap-4">
              <feature.icon className="h-8 w-8" />
              <h3 className="font-bold">{feature.name}</h3>
            </div>
            <p className="mt-2 text-muted-foreground">{feature.description}</p>
          </div>
        ))}
      </div>
    </section>
  );
}