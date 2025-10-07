import React, { useEffect, useMemo, useRef, useState } from 'react'

// helper to build rgba from an "r,g,b" base string
function rgba(base, a) {
  return `rgba(${base},${a})`
}

export function CursorGlow({ color = 'rgba(244,63,94,0.35)' }) {
  const ref = useRef(null)
  useEffect(() => {
    const el = ref.current
    if (!el) return
    let raf
    const onMove = (e) => {
      const x = e.clientX
      const y = e.clientY
      // slight easing for smoothness
      cancelAnimationFrame(raf)
      raf = requestAnimationFrame(() => {
        el.style.transform = `translate(${x - 150}px, ${y - 150}px)`
      })
    }
    window.addEventListener('mousemove', onMove, { passive: true })
    return () => {
      cancelAnimationFrame(raf)
      window.removeEventListener('mousemove', onMove)
    }
  }, [])
  return (
    <div
      ref={ref}
      aria-hidden
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: 300,
        height: 300,
        borderRadius: '50%',
        pointerEvents: 'none',
        background: `radial-gradient(150px 150px at center, ${color}, transparent 60%)`,
        mixBlendMode: 'screen',
        zIndex: 1,
        filter: 'blur(16px)'
      }}
    />
  )
}

// Draw a smooth line trail that follows the mouse and fades over time
export function MouseTrail({ enabled = true, colorBase = '244,63,94', glowBase = '59,130,246' }) {
  const canvasRef = useRef(null)
  const reduced = usePrefersReducedMotionBool()
  useEffect(() => {
    if (!enabled || reduced) return
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    let width = (canvas.width = window.innerWidth)
    let height = (canvas.height = window.innerHeight)

    // trail points with timestamp
    const points = []
    const MAX_AGE = 700 // ms
    const SMOOTHING = 0.15 // interpolation for the virtual cursor
    const MAX_POINTS = 120 // cap for performance
    let vx = width / 2,
      vy = height / 2

    const onResize = () => {
      width = canvas.width = window.innerWidth
      height = canvas.height = window.innerHeight
    }
    const onMove = (e) => {
      // ease a virtual cursor towards the actual cursor for smoothness
      const tx = e.clientX
      const ty = e.clientY
      vx += (tx - vx) * SMOOTHING
      vy += (ty - vy) * SMOOTHING
      points.push({ x: vx, y: vy, t: performance.now() })
      if (points.length > MAX_POINTS) points.shift()
    }
    window.addEventListener('resize', onResize)
    window.addEventListener('mousemove', onMove, { passive: true })

    let raf
    const draw = () => {
      const now = performance.now()
      // fade previous strokes by reducing alpha, without painting any color
      ctx.save()
      ctx.globalCompositeOperation = 'destination-out'
      ctx.fillStyle = 'rgba(0,0,0,0.06)'
      ctx.fillRect(0, 0, width, height)
      ctx.restore()

      // remove old points
      for (let i = points.length - 1; i >= 0; i--) {
        if (now - points[i].t > MAX_AGE) points.splice(i, 1)
      }

      if (points.length > 1) {
        // draw a smoothed polyline using quadratic curves
        ctx.lineCap = 'round'
        ctx.lineJoin = 'round'

        for (let i = 1; i < points.length; i++) {
          const p0 = points[i - 1]
          const p1 = points[i]
          const age = now - p1.t
          const life = 1 - Math.min(age / MAX_AGE, 1)
          const alpha = life * 0.9
          const widthScale = 1 + life * 3 // thicker when fresh
          ctx.strokeStyle = rgba(colorBase, alpha)
          ctx.lineWidth = 1.2 * widthScale
          ctx.beginPath()
          // control point halfway for a smooth curve
          const cx = (p0.x + p1.x) / 2
          const cy = (p0.y + p1.y) / 2
          ctx.moveTo(p0.x, p0.y)
          ctx.quadraticCurveTo(cx, cy, p1.x, p1.y)
          ctx.stroke()
        }

        // subtle outer glow pass using additive blend
  ctx.save()
  ctx.globalCompositeOperation = 'lighter'
        for (let i = 1; i < points.length; i++) {
          const p0 = points[i - 1]
          const p1 = points[i]
          const age = now - p1.t
          const life = 1 - Math.min(age / MAX_AGE, 1)
          const alpha = life * 0.25
          ctx.strokeStyle = rgba(glowBase, alpha)
          ctx.lineWidth = 2.5
          ctx.beginPath()
          const cx = (p0.x + p1.x) / 2
          const cy = (p0.y + p1.y) / 2
          ctx.moveTo(p0.x, p0.y)
          ctx.quadraticCurveTo(cx, cy, p1.x, p1.y)
          ctx.stroke()
        }
        ctx.restore()
      }

      raf = requestAnimationFrame(draw)
    }
    draw()

    return () => {
      cancelAnimationFrame(raf)
      window.removeEventListener('resize', onResize)
      window.removeEventListener('mousemove', onMove)
    }
  }, [enabled])

  return (
    <canvas
      ref={canvasRef}
      aria-hidden
      style={{ position: 'fixed', inset: 0, zIndex: 2, pointerEvents: 'none' }}
    />
  )
}

export function Scanlines() {
  return (
    <div
      aria-hidden
      style={{
        position: 'fixed', inset: 0, pointerEvents: 'none', zIndex: 2,
        backgroundImage: 'repeating-linear-gradient(to bottom, rgba(255,255,255,0.03), rgba(255,255,255,0.03) 1px, transparent 1px, transparent 3px)'
      }}
    />
  )
}

export function Noise() {
  // CSS-animated noise using background-position jitter
  return (
    <div
      aria-hidden
      className="noise-overlay"
  style={{ position: 'fixed', inset: 0, pointerEvents: 'none', zIndex: 1 }}
    />
  )
}

function usePrefersReducedMotion() {
  return useMemo(() =>
    typeof window !== 'undefined' && window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches
  , [])
}

export function MatrixRain({ enabled = true }) {
  const canvasRef = useRef(null)
  const reduced = usePrefersReducedMotion()
  const colorBase = arguments[0]?.colorBase || '244,63,94'

  useEffect(() => {
    if (!enabled || reduced) return
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    let width = canvas.width = window.innerWidth
    let height = canvas.height = window.innerHeight
    let animationFrame
    const fontSize = 14
    const columns = Math.floor(width / fontSize)
    const drops = new Array(columns).fill(1)

    const onResize = () => {
      width = canvas.width = window.innerWidth
      height = canvas.height = window.innerHeight
    }
    window.addEventListener('resize', onResize)

    const draw = () => {
      // translucent background for trail effect
      ctx.fillStyle = 'rgba(0,0,0,0.08)'
      ctx.fillRect(0, 0, width, height)
  ctx.fillStyle = rgba(colorBase, 0.65)
      ctx.font = `${fontSize}px monospace`
      for (let i = 0; i < drops.length; i++) {
        const text = String.fromCharCode(0x30A0 + Math.random() * 96)
        const x = i * fontSize
        const y = drops[i] * fontSize
        ctx.fillText(text, x, y)
        if (y > height && Math.random() > 0.975) drops[i] = 0
        drops[i]++
      }
      animationFrame = requestAnimationFrame(draw)
    }
    draw()

    return () => {
      cancelAnimationFrame(animationFrame)
      window.removeEventListener('resize', onResize)
    }
  }, [enabled, reduced])

  return (
    <canvas
      ref={canvasRef}
      aria-hidden
      style={{ position: 'fixed', inset: 0, zIndex: 0, pointerEvents: 'none', opacity: 0.35 }}
    />
  )
}

function usePrefersReducedMotionBool() {
  if (typeof window === 'undefined' || !window.matchMedia) return false
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches
}

export function Constellation({ enabled = true, colorBase = '244,63,94' }) {
  const canvasRef = useRef(null)
  const reduced = usePrefersReducedMotionBool()
  useEffect(() => {
    if (!enabled || reduced) return
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    let width = canvas.width = window.innerWidth
    let height = canvas.height = window.innerHeight
    const particles = []
    const count = Math.min(120, Math.floor((width * height) / 18000))
    const mouse = { x: width / 2, y: height / 2 }
    for (let i = 0; i < count; i++) {
      particles.push({
        x: Math.random() * width,
        y: Math.random() * height,
        vx: (Math.random() - 0.5) * 0.3,
        vy: (Math.random() - 0.5) * 0.3
      })
    }
    const onMove = (e) => { mouse.x = e.clientX; mouse.y = e.clientY }
    const onResize = () => { width = canvas.width = window.innerWidth; height = canvas.height = window.innerHeight }
    window.addEventListener('mousemove', onMove, { passive: true })
    window.addEventListener('resize', onResize)
    let raf
    const draw = () => {
      ctx.clearRect(0, 0, width, height)
      // draw lines
      for (let i = 0; i < particles.length; i++) {
        const p = particles[i]
        // slight attraction to mouse
        const dx = mouse.x - p.x
        const dy = mouse.y - p.y
        p.vx += (dx / 50000)
        p.vy += (dy / 50000)
        p.x += p.vx
        p.y += p.vy
        if (p.x < 0 || p.x > width) p.vx *= -1
        if (p.y < 0 || p.y > height) p.vy *= -1
      }
      ctx.lineWidth = 1
      for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
          const a = particles[i], b = particles[j]
          const dx = a.x - b.x, dy = a.y - b.y
          const dist2 = dx * dx + dy * dy
          const maxDist2 = 90 * 90
          if (dist2 < maxDist2) {
            const alpha = 1 - dist2 / maxDist2
            ctx.strokeStyle = rgba(colorBase, alpha * 0.35)
            ctx.beginPath()
            ctx.moveTo(a.x, a.y)
            ctx.lineTo(b.x, b.y)
            ctx.stroke()
          }
        }
      }
      // draw points
      for (let i = 0; i < particles.length; i++) {
        const p = particles[i]
        ctx.fillStyle = rgba(colorBase, 0.7)
        ctx.fillRect(p.x, p.y, 2, 2)
      }
      raf = requestAnimationFrame(draw)
    }
    draw()
    return () => { cancelAnimationFrame(raf); window.removeEventListener('mousemove', onMove); window.removeEventListener('resize', onResize) }
  }, [enabled])
  return <canvas ref={canvasRef} aria-hidden style={{ position: 'fixed', inset: 0, zIndex: 0, pointerEvents: 'none', opacity: 0.45 }} />
}

export function ParallaxLayer() {
  const ref = useRef(null)
  useEffect(() => {
    const el = ref.current
    if (!el) return
    let raf
    const onMove = (e) => {
      const x = (e.clientX / window.innerWidth - 0.5) * 8
      const y = (e.clientY / window.innerHeight - 0.5) * 8
      cancelAnimationFrame(raf)
      raf = requestAnimationFrame(() => {
        el.style.transform = `translate3d(${x}px, ${y}px, 0)`
      })
    }
    window.addEventListener('mousemove', onMove, { passive: true })
    return () => { cancelAnimationFrame(raf); window.removeEventListener('mousemove', onMove) }
  }, [])
  return (
    <div
      ref={ref}
      aria-hidden
      style={{
        position: 'fixed', inset: 0, zIndex: 0, pointerEvents: 'none', opacity: 0.25,
        backgroundImage: 'repeating-linear-gradient(135deg, rgba(244,63,94,0.12) 0px, rgba(244,63,94,0.12) 2px, transparent 2px, transparent 10px)'
      }}
    />
  )
}

export function SweepGlow() {
  return (
    <div aria-hidden className="sweep-glow" />
  )
}

export function Vignette() {
  return (
    <div aria-hidden className="vignette" />
  )
}

export function RippleFX({ enabled = true }) {
  const canvasRef = useRef(null)
  const reduced = usePrefersReducedMotionBool()
  useEffect(() => {
    if (!enabled || reduced) return
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    let width = canvas.width = window.innerWidth
    let height = canvas.height = window.innerHeight
    const ripples = []
    const MAX_AGE = 1200 // ms
    const SPEED = 0.6 // pixels per ms

    const onResize = () => {
      width = canvas.width = window.innerWidth
      height = canvas.height = window.innerHeight
    }
    const onClick = (e) => {
      ripples.push({ x: e.clientX, y: e.clientY, t: performance.now() })
    }
    window.addEventListener('resize', onResize)
    window.addEventListener('mousedown', onClick)

    let raf
    const draw = () => {
      const now = performance.now()
      ctx.clearRect(0, 0, width, height)
      ctx.globalCompositeOperation = 'lighter'
      for (let i = ripples.length - 1; i >= 0; i--) {
        const r = ripples[i]
        const age = now - r.t
        if (age > MAX_AGE) { ripples.splice(i, 1); continue }
        const prog = age / MAX_AGE
        const radius = age * SPEED
        const alpha = (1 - prog) * 0.35

        // outer soft glow
        const grad = ctx.createRadialGradient(r.x, r.y, Math.max(radius - 40, 0), r.x, r.y, radius + 60)
        grad.addColorStop(0, `rgba(244,63,94,${alpha * 0.35})`)
        grad.addColorStop(0.5, `rgba(59,130,246,${alpha * 0.25})`)
        grad.addColorStop(1, 'rgba(0,0,0,0)')
        ctx.fillStyle = grad
        ctx.beginPath()
        ctx.arc(r.x, r.y, radius + 60, 0, Math.PI * 2)
        ctx.fill()

        // ring ripples
        ctx.lineWidth = 2
        const rings = 3
        for (let k = 0; k < rings; k++) {
          const ringR = radius - k * 24
          if (ringR <= 0) continue
          const a = Math.max(alpha - k * 0.08, 0)
          ctx.strokeStyle = `rgba(244,63,94,${a})`
          ctx.beginPath()
          ctx.arc(r.x, r.y, ringR, 0, Math.PI * 2)
          ctx.stroke()
        }
      }
      ctx.globalCompositeOperation = 'source-over'
      raf = requestAnimationFrame(draw)
    }
    draw()

    return () => {
      cancelAnimationFrame(raf)
      window.removeEventListener('resize', onResize)
      window.removeEventListener('mousedown', onClick)
    }
  }, [enabled])
  return (
    <canvas
      ref={canvasRef}
      aria-hidden
      style={{ position: 'fixed', inset: 0, zIndex: 2, pointerEvents: 'none' }}
    />
  )
}

export default function VisualFX({
  palette = 'red',
  flags = {},
  matrix = true,
  noise = true,
  scanlines = true,
}) {
  // color bases are simple "r,g,b" strings to combine with varying alpha
  const colors = palette === 'blue'
    ? { primary: '59,130,246', secondary: '244,63,94' }
    : { primary: '244,63,94', secondary: '59,130,246' }
  const [enableMatrix, setEnableMatrix] = useState(() => typeof window !== 'undefined' ? window.innerWidth >= 768 : true)
  useEffect(() => {
    const onResize = () => setEnableMatrix(window.innerWidth >= 768)
    window.addEventListener('resize', onResize)
    return () => window.removeEventListener('resize', onResize)
  }, [])
  return (
    <>
      {/* Base layers (furthest back) */}
      {flags.parallax !== false && <ParallaxLayer />}
      {flags.vignette !== false && <Vignette />}
      {flags.sweep !== false && <SweepGlow />}
      {(flags.matrix !== false && matrix) && <MatrixRain enabled={enableMatrix} colorBase={colors.primary} />}
      {flags.constellation !== false && <Constellation colorBase={colors.primary} />}
      {flags.ripple !== false && <RippleFX />}
      {flags.mouseTrail !== false && (
        <MouseTrail enabled={true} colorBase={colors.primary} glowBase={colors.secondary} />
      )}
      {(flags.noise !== false && noise) && <Noise />}
      {(flags.scanlines !== false && scanlines) && <Scanlines />}
    </>
  )
}
