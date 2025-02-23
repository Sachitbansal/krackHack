'use client'


import { Button } from "@/components/ui/button"

export default function CTA() {
  return (
    <section className="border-t">
      <div className="container flex flex-col items-center gap-4 py-24 text-center md:py-32">
        <h2 className="font-bold text-3xl leading-[1.1] sm:text-3xl md:text-5xl">
          Ready to revolutionize your business?
        </h2>
        <p className="max-w-[42rem] leading-normal text-muted-foreground sm:text-xl sm:leading-8">
          Join leading companies who trust WebBuidler to drive their digital transformation and stay ahead in the
          rapidly evolving tech landscape.
        </p>
        {/* add button.onclic to redirect to /generate */}
        <Button size="lg" className="mt-4" onClick={() => window.location.href = "/generate"}>
          Get Started Today
        </Button>
      </div>
    </section>
  )
}

