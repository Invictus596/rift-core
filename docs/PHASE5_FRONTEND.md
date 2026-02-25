# Phase 5: Frontend Dashboard

> **Visual Interface for the Listen-Verify-Execute Pipeline**

---

## 🎯 Overview

**Phase 5** introduces a modern, responsive frontend dashboard built with **Next.js**, providing real-time visualization of the Rift Protocol pipeline. The UI enables users to monitor Bitcoin mempool activity, track verification status on Starknet, and observe the complete Listen-Verify-Execute flow.

### Key Features

- 📊 **Real-time Monitoring** - Live updates from the Watcher service
- 🎨 **Modern UI** - Tailwind CSS + shadcn/ui components
- 📐 **Bento Grid Layout** - Modular architecture visualization
- 🚀 **21st.dev Components** - Pre-built Hero section and data grids
- ⚡ **Instant Feedback** - Sub-second UI updates for detected transactions

---

## 🏗️ Architecture

```
┌─────────────────┐     ┌──────────────┐     ┌─────────────────┐
│  Bitcoin Node   │────▶│ Rift Watcher │────▶│  Frontend API   │
│  (Mempool)      │     │  (Python)    │     │  (Next.js)      │
└─────────────────┘     └──────────────┘     └─────────────────┘
                              │                     │
                              │                     ▼
                              │            ┌─────────────────┐
                              │            │ Dashboard UI    │
                              │            │ (React/Tailwind)│
                              │            └─────────────────┘
                              │
                              ▼
                       ┌──────────────┐
                       │ Starknet RPC │
                       │ (Verifier)   │
                       └──────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Framework** | Next.js 15+ | React framework with App Router |
| **Styling** | Tailwind CSS | Utility-first CSS framework |
| **UI Components** | shadcn/ui | Accessible, customizable components |
| **Pre-built UI** | 21st.dev | Hero section, Bento Grid layouts |
| **State Management** | React Query | Data fetching and caching |
| **Real-time Updates** | WebSocket/SSE | Live mempool monitoring |
| **Charts** | Recharts | Verification metrics visualization |

---

## 📁 Project Structure

```
frontend/
├── app/                        # Next.js App Router
│   ├── layout.tsx              # Root layout with providers
│   ├── page.tsx                # Main dashboard (Hero + Bento Grid)
│   ├── api/                    # API routes
│   │   └── stats/              # Verification statistics endpoint
│   └── globals.css             # Global styles (Tailwind)
├── components/
│   ├── ui/                     # shadcn/ui components
│   │   ├── card.tsx            # Card containers
│   │   ├── button.tsx          # Action buttons
│   │   └── table.tsx           # Data tables
│   ├── hero.tsx                # 21st.dev Hero section
│   ├── bento-grid.tsx          # Architecture visualization
│   ├── stats-card.tsx          # Verification metrics
│   └── transaction-list.tsx    # Recent detections
├── lib/
│   ├── api.ts                  # API client (Watcher bridge)
│   └── utils.ts                # Helper functions
├── public/                     # Static assets
├── package.json                # Dependencies
├── tailwind.config.ts          # Tailwind configuration
└── tsconfig.json               # TypeScript config
```

---

## 🎨 Component Design

### Hero Section (21st.dev)

The landing page features a **Hero section** from 21st.dev, providing:

- Bold headline: "Making Bitcoin Instant"
- Subtitle explaining the value proposition
- Call-to-action buttons (View Demo, Documentation)
- Animated background elements

```tsx
// components/hero.tsx
import { Hero } from "@21st-dev/ui";

export function DashboardHero() {
  return (
    <Hero
      title="Making Bitcoin Instant"
      subtitle="Break the 10-minute barrier with Rift Protocol"
      cta={[
        { label: "View Demo", href: "/demo" },
        { label: "Documentation", href: "/docs" }
      ]}
    />
  );
}
```

---

### Bento Grid Architecture

The **Bento Grid** layout visualizes the complete pipeline in a modular, easy-to-understand format:

```tsx
// components/bento-grid.tsx
import { BentoGrid, BentoCard } from "@21st-dev/ui";

const grid = [
  {
    name: "Bitcoin Mempool",
    description: "Real-time transaction monitoring",
    icon: <BitcoinIcon />,
    data: { currentSize: 45230 }
  },
  {
    name: "RIFT Detections",
    description: "Pattern recognition in OP_RETURN",
    icon: <SearchIcon />,
    data: { today: 1247, accuracy: "100%" }
  },
  {
    name: "Starknet Verifier",
    description: "ZK-proof signature verification",
    icon: <ShieldIcon />,
    data: { verified: 892, pending: 3 }
  },
  {
    name: "Executor",
    description: "Instant wrapped asset minting",
    icon: <ZapIcon />,
    data: { minted: 156, volume: "$2.3M" }
  }
];

export function ArchitectureGrid() {
  return <BentoGrid items={grid} />;
}
```

**Grid Layout:**
```
┌─────────────────────┬─────────────────────┐
│   Bitcoin Mempool   │   RIFT Detections   │
│   (Live Size)       │   (Today's Count)   │
├─────────────────────┴─────────────────────┤
│           Starknet Verifier               │
│        (Verified / Pending)               │
├─────────────────────┬─────────────────────┤
│     Executor        │   Verification      │
│   (Minted Assets)   │      Chart          │
└─────────────────────┴─────────────────────┘
```

---

## 📊 Key Dashboard Views

### 1. Overview Dashboard

**Purpose**: High-level system status

**Metrics Displayed**:
- Current mempool size
- RIFT transactions detected (24h)
- Verifications completed
- Average latency

**Components**: Stats cards, line chart, recent activity table

---

### 2. Transaction Monitor

**Purpose**: Real-time detection feed

**Features**:
- Live transaction stream
- Filter by status (Detected, Verified, Executed)
- Search by transaction ID
- OP_RETURN data viewer

**Components**: Data table, search input, status badges

---

### 3. Verification Stats

**Purpose**: Analytics and performance metrics

**Charts**:
- Verifications over time (line chart)
- Detection accuracy (pie chart)
- Latency distribution (histogram)

**Components**: Recharts components, time range selector

---

## 🔌 API Integration

### Watcher Bridge API

The frontend communicates with the Python Watcher via a REST API:

```typescript
// lib/api.ts
const WATCHER_API = "http://localhost:8000";

export async function getStats() {
  const res = await fetch(`${WATCHER_API}/stats`);
  return res.json();
}

export async function getRecentDetections(limit = 50) {
  const res = await fetch(`${WATCHER_API}/detections?limit=${limit}`);
  return res.json();
}

export async function getVerification(txHash: string) {
  const res = await fetch(`${WATCHER_API}/verification/${txHash}`);
  return res.json();
}
```

### WebSocket for Real-time Updates

```typescript
// components/live-monitor.tsx
useEffect(() => {
  const ws = new WebSocket("ws://localhost:8000/ws");
  
  ws.onmessage = (event) => {
    const detection = JSON.parse(event.data);
    setDetections((prev) => [detection, ...prev]);
  };
  
  return () => ws.close();
}, []);
```

---

## 🎨 Design System

### Color Palette

| Color | Hex | Usage |
|-------|-----|-------|
| Bitcoin Orange | `#F7931A` | Primary actions, Bitcoin-related |
| Starknet Blue | `#3B3C97` | Secondary actions, L2-related |
| Success Green | `#10B981` | Verified transactions |
| Warning Yellow | `#F59E0B` | Pending verifications |
| Error Red | `#EF4444` | Failed verifications |

### Typography

- **Headings**: `font-sans` (Inter)
- **Body**: `font-sans` (Inter)
- **Code**: `font-mono` (JetBrains Mono)

### Spacing

- Base unit: `4px` (Tailwind default)
- Card padding: `p-6` (24px)
- Grid gap: `gap-4` (16px)

---

## 🚀 Getting Started

### Prerequisites

```bash
# Node.js 18+ required
node --version  # v18.0.0 or higher

# pnpm recommended
pnpm --version
```

### Installation

```bash
cd frontend

# Install dependencies
pnpm install

# Run development server
pnpm dev

# Open http://localhost:3000
```

### Build for Production

```bash
# Build optimized bundle
pnpm build

# Preview production build
pnpm start
```

---

## 📦 Dependencies

```json
{
  "dependencies": {
    "next": "^15.0.0",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "@radix-ui/react-card": "^1.0.0",
    "@radix-ui/react-table": "^1.0.0",
    "tailwindcss": "^3.4.0",
    "recharts": "^2.10.0",
    "@tanstack/react-query": "^5.0.0",
    "@21st-dev/ui": "^0.1.0"
  },
  "devDependencies": {
    "typescript": "^5.0.0",
    "@types/node": "^20.0.0",
    "@types/react": "^19.0.0",
    "eslint": "^8.0.0"
  }
}
```

---

## 🔧 Configuration

### Tailwind Config

```typescript
// tailwind.config.ts
import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        bitcoin: "#F7931A",
        starknet: "#3B3C97",
      },
    },
  },
  plugins: [],
};

export default config;
```

---

## 📈 Performance Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| First Contentful Paint | <1.5s | Lighthouse |
| Time to Interactive | <3.0s | Lighthouse |
| WebSocket Latency | <100ms | Chrome DevTools |
| API Response Time | <200ms | React Query |

---

## 🎯 Roadmap

### Completed ✅

- [x] Next.js project initialization
- [x] Tailwind CSS configuration
- [x] shadcn/ui component setup
- [x] 21st.dev integration

### In Progress 📋

- [ ] Hero section implementation
- [ ] Bento Grid architecture visualization
- [ ] Watcher API integration
- [ ] Real-time WebSocket updates

### Planned 🔜

- [ ] Verification stats dashboard
- [ ] Transaction history table
- [ ] Mobile responsive design
- [ ] Dark mode toggle
- [ ] Export functionality (CSV, PDF)

---

## 🤝 Contributing

### Component Guidelines

1. **Use shadcn/ui** for base components (Card, Button, Table)
2. **Follow 21st.dev patterns** for complex layouts
3. **TypeScript strict mode** for all components
4. **Tailwind CSS** for styling (no inline styles)
5. **React Query** for data fetching

### Code Style

```tsx
// ✅ Good: Typed props, shadcn components
interface StatsCardProps {
  title: string;
  value: number;
  change: number;
}

export function StatsCard({ title, value, change }: StatsCardProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value}</div>
        <p className={cn(change > 0 ? "text-green-600" : "text-red-600")}>
          {change > 0 ? "+" : ""}{change}%
        </p>
      </CardContent>
    </Card>
  );
}
```

---

## 📚 Related Documentation

| Document | Description |
|----------|-------------|
| [Technical Overview](TECHNICAL_OVERVIEW.md) | Full project overview |
| [Architecture](architecture.md) | System design details |
| [Getting Started](getting_started.md) | Development setup |
| [Watcher README](../watcher/README.md) | Backend API reference |

---

## 🎬 Demo Preview

### Dashboard Screenshot (Conceptual)

```
┌─────────────────────────────────────────────────────────────┐
│  ⚡ Rift Protocol                    [Demo] [Documentation]  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│         Making Bitcoin Instant                              │
│   Break the 10-minute barrier with Rift Protocol            │
│                                                             │
│          [View Live Demo]  [Read Docs]                      │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐                        │
│  │ 🟠 Bitcoin   │  │ 🔍 RIFT      │                        │
│  │ Mempool      │  │ Detections   │                        │
│  │ 45,230 txs   │  │ 1,247 today  │                        │
│  └──────────────┘  └──────────────┘                        │
│  ┌──────────────────────────────┐                          │
│  │ 🛡️ Starknet Verifier        │                          │
│  │ ✅ 892 verified  ⏳ 3 pending│                          │
│  └──────────────────────────────┘                          │
│  ┌──────────────┐  ┌──────────────┐                        │
│  │ ⚡ Executor  │  │ 📊 Stats     │                        │
│  │ 156 minted   │  │ [Line Chart] │                        │
│  │ $2.3M volume │  │              │                        │
│  └──────────────┘  └──────────────┘                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

**Phase 5 Status**: In Development 🚧

*Last Updated: February 25, 2026*
