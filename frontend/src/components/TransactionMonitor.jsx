import React, { useState, useEffect } from 'react'
import axios from 'axios'

const API_URL = 'http://localhost:8000'

function TransactionMonitor() {
  const [transactions, setTransactions] = useState([])
  const [loading, setLoading] = useState(true)
  
  useEffect(() => {
    fetchTransactions()
    const interval = setInterval(fetchTransactions, 5000)
    return () => clearInterval(interval)
  }, [])
  
  const fetchTransactions = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/transactions?limit=50`)
      setTransactions(response.data)
      setLoading(false)
    } catch (error) {
      console.error('Error fetching transactions:', error)
    }
  }
  
  const getStatusBadge = (status) => {
    const styles = {
      approved: 'bg-green-100 text-green-800',
      blocked: 'bg-red-100 text-red-800',
      flagged: 'bg-yellow-100 text-yellow-800',
      pending: 'bg-gray-100 text-gray-800'
    }
    return `px-2 py-1 rounded-full text-xs font-medium ${styles[status] || styles.pending}`
  }
  
  if (loading) return <div className="text-center py-8">Loading transactions...</div>
  
  return (
    <div className="bg-white rounded-lg shadow">
      <div className="px-6 py-4 border-b border-gray-200">
        <h2 className="text-xl font-semibold">Live Transaction Monitor</h2>
        <p className="text-gray-600 text-sm">Real-time transaction fraud detection status</p>
      </div>
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Phone</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Amount</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Risk Score</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Time</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {transactions.map((tx) => (
              <tr key={tx.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 text-sm text-gray-900">{tx.id}</td>
                <td className="px-6 py-4 text-sm text-gray-900">{tx.phone_number}</td>
                <td className="px-6 py-4 text-sm text-gray-900">{tx.currency} {tx.amount}</td>
                <td className="px-6 py-4"><span className={getStatusBadge(tx.status)}>{tx.status}</span></td>
                <td className="px-6 py-4">
                  <div className="flex items-center">
                    <div className="w-16 bg-gray-200 rounded-full h-2">
                      <div className={`h-2 rounded-full ${tx.risk_score > 70 ? 'bg-red-600' : tx.risk_score > 40 ? 'bg-yellow-500' : 'bg-green-500'}`} style={{ width: `${tx.risk_score}%` }}></div>
                    </div>
                    <span className="ml-2 text-sm">{tx.risk_score}</span>
                  </div>
                </td>
                <td className="px-6 py-4 text-sm text-gray-500">{new Date(tx.created_at).toLocaleTimeString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default TransactionMonitor