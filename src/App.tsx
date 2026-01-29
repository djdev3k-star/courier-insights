import { Routes, Route } from 'react-router-dom'
import { Layout } from './components/Layout'
import { Dashboard } from './pages/Dashboard'
import { Schedule } from './pages/Schedule'
import { Expenses } from './pages/Expenses'
import { Performance } from './pages/Performance'
import { Reports } from './pages/Reports'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Dashboard />} />
        <Route path="schedule" element={<Schedule />} />
        <Route path="expenses" element={<Expenses />} />
        <Route path="performance" element={<Performance />} />
        <Route path="reports" element={<Reports />} />
      </Route>
    </Routes>
  )
}

export default App
