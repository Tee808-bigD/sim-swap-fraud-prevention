import React, { useState } from 'react'
import axios from 'axios'

const API_URL = 'http://localhost:8000'

function AgentPortal() {
  const [formData, setFormData] = useState({
    phone_number: '',
    amount: '',
    currency: 'KES',
    transaction_type: 'send',
    recipient: '',
    is_new_recipient: false
  })
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  
  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setResult(null)
    
    try {
      const response = await axios.post(`${API_URL}/api/transactions`, {
        ...formData,
        amount: parseFloat(formData.amount)
      })
      setResult(response.data)
    } catch (error) {
      setResult({ error: 'Failed to process transaction' })
    } finally {
      setLoading(false)
    }
  }
  
  const getRiskColor = (status) => {
    switch(status) {
      case 'approved': return 'bg-green-100 border-green-500 text-green-700'
      case 'blocked': return 'bg-red-100 border-red-500 text-red-700'
      case 'flagged': return 'bg-yellow-100 border-yellow-500 text-yellow-700'
      default: return 'bg-gray-100 border-gray-500'
    }
  }
  
  return (
    <div className="max-w-2xl mx-auto">
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-2xl font-bold mb-6">Mobile Money Agent Portal</h2>
        <p className="text-gray-600 mb-6">Check transactions for SIM swap fraud before processing</p>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Phone Number</label>
            <input
              type="tel"
              required
              value={formData.phone_number}
              onChange={(e) => setFormData({...formData, phone_number: e.target.value})}
              placeholder="+254XXXXXXXXX or +99999991000 (test)"
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-2 border"
            />
          </div>
          
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Amount</label>
              <input
                type="number"
                required
                value={formData.amount}
                onChange={(e) => setFormData({...formData, amount: e.target.value})}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-2 border"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Currency</label>
              <select
                value={formData.currency}
                onChange={(e) => setFormData({...formData, currency: e.target.value})}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-2 border"
              >
                <option>KES</option>
                <option>UGX</option>
                <option>TZS</option>
                <option>NGN</option>
                <option>ZAR</option>
              </select>
            </div>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700">Recipient</label>
            <input
              type="text"
              value={formData.recipient}
              onChange={(e) => setFormData({...formData, recipient: e.target.value})}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-2 border"
            />
          </div>
          
          <div className="flex items-center">
            <input
              type="checkbox"
              checked={formData.is_new_recipient}
              onChange={(e) => setFormData({...formData, is_new_recipient: e.target.checked})}
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <label className="ml-2 block text-sm text-gray-700">New recipient (never sent to before)</label>
          </div>
          
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? 'Checking...' : 'Check Transaction'}
          </button>
        </form>
        
        {result && !result.error && (
          <div className={`mt-6 p-4 rounded-lg border-l-4 ${getRiskColor(result.status)}`}>
            <div className="flex justify-between items-start">
              <div>
                <h3 className="font-bold text-lg">Decision: {result.status.toUpperCase()}</h3>
                <p className="mt-2">Risk Score: {result.risk_score}/100</p>
              </div>
              <div className="text-right">
                <p className="text-sm">Transaction ID: {result.id}</p>
                <p className="text-sm">Amount: {result.currency} {result.amount}</p>
              </div>
            </div>
            
            {result.status === 'blocked' && (
              <div className="mt-3 p-3 bg-red-50 rounded">
                <p className="font-semibold">⚠️ Transaction Blocked</p>
                <p className="text-sm mt-1">This transaction has been blocked due to high fraud risk.</p>
              </div>
            )}
            
            {result.status === 'flagged' && (
              <div className="mt-3 p-3 bg-yellow-50 rounded">
                <p className="font-semibold">⚠️ Manual Review Required</p>
                <p className="text-sm mt-1">Please verify customer identity before proceeding.</p>
              </div>
            )}
            
            {result.status === 'approved' && (
              <div className="mt-3 p-3 bg-green-50 rounded">
                <p className="font-semibold">✓ Transaction Approved</p>
                <p className="text-sm mt-1">No fraud indicators detected. You may proceed.</p>
              </div>
            )}
          </div>
        )}
        
        {result && result.error && (
          <div className="mt-6 p-4 bg-red-100 border border-red-400 rounded">
            <p className="text-red-700">{result.error}</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default AgentPortal