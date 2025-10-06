import React, { useEffect, useMemo, useState } from 'react'
const API_BASE = import.meta.env.VITE_API_BASE || '/api'

const Section = ({ title, children }) => (
  <div className="card">
    <div className="flex items-center justify-between mb-4">
      <h2 className="text-xl font-semibold text-redcalibur-300">{title}</h2>
    </div>
    {children}
  </div>
)

const Header = ({ apiStatus }) => (
  <header className="sticky top-0 z-10 backdrop-blur bg-black/60 border-b border-zinc-800">
    <div className="max-w-7xl mx-auto px-4 py-4 flex items-center gap-3">
      <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M12 2L4 6v5c0 5.55 3.84 10.74 8 12 4.16-1.26 8-6.45 8-12V6l-8-4z" fill="#e11d48"/>
        <path d="M12 6v12M9 10h6" stroke="#fff" strokeWidth="1.5" strokeLinecap="round"/>
      </svg>
      <div className="flex items-center gap-3">
        <div className="text-2xl font-bold tracking-tight">RedCalibur</div>
        <div className="text-sm text-zinc-400 -mt-1">Red Teaming AI — Recon, Scan, Report</div>
        <span className="ml-2 inline-flex items-center gap-2 text-xs px-2 py-1 rounded-full border border-zinc-700 bg-zinc-900/70">
          <span className={`inline-block w-2.5 h-2.5 rounded-full ${apiStatus === 'ok' ? 'bg-green-500' : apiStatus === 'down' ? 'bg-redcalibur-500' : 'bg-zinc-500'}`}></span>
          API
        </span>
      </div>
    </div>
  </header>
)

export default function App() {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [logs, setLogs] = useState([])
  const [apiStatus, setApiStatus] = useState('unknown')

  const api = useMemo(() => ({
    post: async (path, body, { updateResult = true } = {}) => {
      setLoading(true)
      const start = performance.now()
      try {
        const res = await fetch(`${API_BASE}${path}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(body)
        })
        const json = await res.json()
        if (!res.ok) throw new Error(json?.detail || 'Request failed')
        if (updateResult) setResult(json)
        setLogs(l => [{ time: new Date().toLocaleTimeString(), path, ok: true, ms: Math.round(performance.now() - start) }, ...l])
        return json
      } catch (e) {
        setLogs(l => [{ time: new Date().toLocaleTimeString(), path, ok: false, error: e.message }, ...l])
        throw e
      } finally {
        setLoading(false)
      }
    }
  }), [])

  // API health probe
  useEffect(() => {
    let mounted = true
    const ping = async () => {
      try {
        const res = await fetch(`${API_BASE}/health`)
        if (!mounted) return
        setApiStatus(res.ok ? 'ok' : 'down')
      } catch {
        if (!mounted) return
        setApiStatus('down')
      }
    }
    ping()
    const id = setInterval(ping, 10000)
    return () => { mounted = false; clearInterval(id) }
  }, [])

  return (
    <div>
      <Header apiStatus={apiStatus} />
      <main className="max-w-7xl mx-auto px-4 py-6 grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="space-y-6">
          <Section title="Domain Reconnaissance">
            <DomainForm onSubmit={(data) => api.post('/domain', data)} loading={loading} />
          </Section>
          <Section title="Network Scan">
            <ScanForm onSubmit={(data) => api.post('/scan', data)} loading={loading} />
          </Section>
          <Section title="Username Lookup">
            <UsernameForm onSubmit={(data) => api.post('/username', data)} loading={loading} />
          </Section>
          <Section title="URL Malware Scan (VirusTotal)">
            <URLScanForm onSubmit={(data) => api.post('/urlscan', data)} loading={loading} />
          </Section>
        </div>

        <div className="space-y-6">
          <Section title="Results">
            {result ? <ResultViewer data={result} /> : <Placeholder />}
            {result && (
              <div className="mt-4">
                <button className="btn" onClick={async () => {
                  await api.post('/summarize', { payload: result }, { updateResult: false })
                    .then((r) => setResult(prev => ({ ...prev, ai_summary: r?.summary })))
                    .catch(() => {})
                }}>AI Summarize</button>
              </div>
            )}
          </Section>
          <Section title="Activity Log">
            <Logs logs={logs} />
          </Section>
        </div>
      </main>
    </div>
  )
}

function Field({ label, children }) {
  return (
    <label className="block mb-3">
      <div className="text-sm text-zinc-300 mb-1">{label}</div>
      {children}
    </label>
  )
}

function DomainForm({ onSubmit, loading }) {
  const [target, setTarget] = useState('example.com')
  const [flags, setFlags] = useState({ whois: true, dns: true, subdomains: false, ssl: true, all: false })

  return (
    <form onSubmit={async (e) => { e.preventDefault(); await onSubmit({ target, ...flags }) }}>
      <Field label="Domain">
        <input className="input" placeholder="example.com" value={target} onChange={e=>setTarget(e.target.value)} />
      </Field>
      <div className="grid grid-cols-2 gap-3 mb-4">
        {['whois','dns','subdomains','ssl','all'].map(k => (
          <label key={k} className="flex items-center gap-2 text-sm">
            <input type="checkbox" checked={flags[k]} onChange={()=>setFlags(f=>({ ...f, [k]: !f[k] }))} />
            <span className="capitalize">{k}</span>
          </label>
        ))}
      </div>
      <button className="btn" disabled={loading}>{loading ? 'Running…' : 'Run Recon'}</button>
    </form>
  )
}

function ScanForm({ onSubmit, loading }) {
  const [target, setTarget] = useState('1.1.1.1')
  const [ports, setPorts] = useState('80,443,22')
  const [shodan, setShodan] = useState(false)

  return (
    <form onSubmit={async (e)=>{e.preventDefault(); const p = ports.split(',').map(x=>parseInt(x.trim())).filter(Boolean); await onSubmit({ target, ports:p, shodan })}}>
      <Field label="Target IP or Hostname">
        <input className="input" value={target} onChange={e=>setTarget(e.target.value)} />
      </Field>
      <Field label="Ports (comma-separated)">
        <input className="input" value={ports} onChange={e=>setPorts(e.target.value)} />
      </Field>
      <label className="flex items-center gap-2 text-sm mb-4">
        <input type="checkbox" checked={shodan} onChange={()=>setShodan(v=>!v)} /> Use Shodan
      </label>
      <button className="btn" disabled={loading}>{loading ? 'Scanning…' : 'Run Scan'}</button>
    </form>
  )
}

function UsernameForm({ onSubmit, loading }) {
  const [target, setTarget] = useState('johndoe')
  const [platforms, setPlatforms] = useState('twitter,linkedin,github')
  return (
    <form onSubmit={async (e)=>{e.preventDefault(); await onSubmit({ target, platforms: platforms.split(',').map(x=>x.trim()).filter(Boolean) })}}>
      <Field label="Username">
        <input className="input" value={target} onChange={e=>setTarget(e.target.value)} />
      </Field>
      <Field label="Platforms (comma-separated)">
        <input className="input" value={platforms} onChange={e=>setPlatforms(e.target.value)} />
      </Field>
      <button className="btn" disabled={loading}>{loading ? 'Searching…' : 'Lookup'}</button>
    </form>
  )
}

function URLScanForm({ onSubmit, loading }) {
  const [url, setUrl] = useState('http://example.com')
  return (
    <form onSubmit={async (e)=>{e.preventDefault(); await onSubmit({ url })}}>
      <Field label="URL">
        <input className="input" value={url} onChange={e=>setUrl(e.target.value)} />
      </Field>
      <button className="btn" disabled={loading}>{loading ? 'Submitting…' : 'Scan URL'}</button>
    </form>
  )
}

function ResultViewer({ data }) {
  return (
    <div className="bg-black/40 border border-zinc-800 rounded-lg">
      <pre className="text-sm p-4 overflow-auto max-h-[480px]">{JSON.stringify(data, null, 2)}</pre>
    </div>
  )
}

function Logs({ logs }) {
  if (!logs.length) return <div className="text-zinc-400">No activity yet.</div>
  return (
    <ul className="space-y-2 text-sm">
      {logs.map((l, i) => (
        <li key={i} className="flex items-center justify-between bg-zinc-900/50 border border-zinc-800 rounded-md px-3 py-2">
          <span className={l.ok ? 'text-green-400' : 'text-redcalibur-400'}>
            {l.ok ? 'OK' : 'ERR'} <span className="text-zinc-400">{l.path}</span>
          </span>
          <span className="text-zinc-500">{l.ms ? `${l.ms}ms` : ''} — {l.time}</span>
        </li>
      ))}
    </ul>
  )
}

function Placeholder() {
  return (
    <div className="text-zinc-400">
      Trigger any action from the left. Results will appear here.
    </div>
  )
}
