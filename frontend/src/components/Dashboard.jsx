import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'

const API_URL = 'http://localhost:8000'

function Dashboard() {
  const [stats, setStats] = useState(null)
  const [timeline, setTimeline] = useState([])
  const [loading, setLoading] = useState(true)
  
  useEffect(() => {
    fetchDashboardData()
    const interval = setInterval(fetchDashboardData, 10000)
    return () => clearInterval(interval)
  }, [])
  
  const fetchDashboardData = async () => {
    try {
      const [statsRes, timelineRes] = await Promise.all([
        axios.get(`${API_URL}/api/dashboard/stats`),
        axios.get(`${API_URL}/api/dashboard/timeline`)
      ])
      setStats(statsRes.data)
      setTimeline(timelineRes.data)
      setLoading(false)
    } catch (error) {
      console.error('Error fetching dashboard data:', error)
    }
  }
  
  if (loading) return <div className="flex justify-center items-center h-64">Loading dashboard...</div>
  
  const pieData = [
    { name: 'Approved', value: stats.approved, color: '#10B981' },
    { name: 'Blocked', value: stats.blocked, color: '#EF4444' },
    { name: 'Flagged', value: stats.flagged, color: '#F59E0B' }
  ]
  
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-gray-500 text-sm">Total Transactions</div>
          <div className="text-3xl font-bold text-gray-800">{stats.total_transactions}</div>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-gray-500 text-sm">Fraud Blocked</div>
          <div className="text-3xl font-bold text-red-600">{stats.blocked}</div>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-gray-500 text-sm">Approval Rate</div>
          <div className="text-3xl font-bold text-green-600">{stats.approval_rate}%</div>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-gray-500 text-sm">Estimated Savings</div>
          <div className="text-3xl font-bold text-blue-600">${stats.total_amount_saved.toLocaleString()}</div>
        </div>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold mb-4">Transaction Timeline</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={timeline}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="total" stroke="#3B82F6" name="Total" />
              <Line type="monotone" dataKey="blocked" stroke="#EF4444" name="Blocked" />
              <Line type="monotone" dataKey="approved" stroke="#10B981" name="Approved" />
            </LineChart>
          </ResponsiveContainer>
        </div>
        
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold mb-4">Transaction Status</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie data={pieData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={100} label>
                {pieData.map((entry, index) => <Cell key={`cell-${index}`} fill={entry.color} />)}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  )
}

export default Dashboard