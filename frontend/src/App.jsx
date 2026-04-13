import React, { useState, useEffect } from 'react'

function App() {
  const [phone, setPhone] = useState('')
  const [amount, setAmount] = useState('')
  const [isNew, setIsNew] = useState(false)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const checkTransaction = async (e) => {
    e.preventDefault()
    setLoading(true)
    try {
      const res = await fetch('http://localhost:8000/api/transactions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          phone_number: phone,
          amount: parseFloat(amount),
          currency: 'KES',
          is_new_recipient: isNew
        })
      })
      const data = await res.json()
      setResult(data)
    } catch (err) {
      setResult({ error: 'Backend not running. Start with: uvicorn app.main:app --reload --port 8000' })
    }
    setLoading(false)
  }

  return (
    <div style={{ fontFamily: 'Arial', maxWidth: '500px', margin: '50px auto', padding: '20px' }}>
      <h1 style={{ color: '#2563eb' }}>SimGuard</h1>
      <p>SIM Swap Fraud Prevention for Mobile Money</p>
      
      <form onSubmit={checkTransaction} style={{ marginTop: '30px' }}>
        <div style={{ marginBottom: '15px' }}>
          <label>Phone Number:</label><br/>
          <input 
            type="text" 
            value={phone} 
            onChange={(e) => setPhone(e.target.value)} 
            required
            style={{ width: '100%', padding: '8px', marginTop: '5px' }}
            placeholder="+99999991000"
          />
          <small>Test: +99999991000 (fraud) | +99999991001 (safe)</small>
        </div>
        
        <div style={{ marginBottom: '15px' }}>
          <label>Amount:</label><br/>
          <input 
            type="number" 
            value={amount} 
            onChange={(e) => setAmount(e.target.value)} 
            required
            style={{ width: '100%', padding: '8px', marginTop: '5px' }}
          />
        </div>
        
        <div style={{ marginBottom: '15px' }}>
          <label>
            <input 
              type="checkbox" 
              checked={isNew} 
              onChange={(e) => setIsNew(e.target.checked)} 
            />
            New recipient (higher risk)
          </label>
        </div>
        
        <button 
          type="submit" 
          disabled={loading}
          style={{ 
            background: '#2563eb', 
            color: 'white', 
            padding: '10px 20px', 
            border: 'none', 
            borderRadius: '5px',
            cursor: 'pointer'
          }}
        >
          {loading ? 'Checking...' : 'Check Transaction'}
        </button>
      </form>
      
      {result && !result.error && (
        <div style={{ 
          marginTop: '20px', 
          padding: '15px', 
          borderRadius: '5px',
          background: result.status === 'approved' ? '#d1fae5' : result.status === 'blocked' ? '#fee2e2' : '#fef3c7',
          borderLeft: `4px solid ${result.status === 'approved' ? '#10b981' : result.status === 'blocked' ? '#ef4444' : '#f59e0b'}`
        }}>
          <h3>Decision: {result.status.toUpperCase()}</h3>
          <p>Risk Score: {result.risk_score}/100</p>
          <p>{result.message}</p>
        </div>
      )}
      
      {result && result.error && (
        <div style={{ marginTop: '20px', padding: '15px', background: '#fee2e2', borderRadius: '5px', color: 'red' }}>
          {result.error}
        </div>
      )}
    </div>
  )
}

export default App