import React, { useState, useEffect } from 'react'
import axios from 'axios'

const API_URL = 'http://localhost:8000'

function FraudAlertFeed() {
  const [alerts, setAlerts] = useState([])
  const [loading, setLoading] = useState(true)
  
  useEffect(() => {
    fetchAlerts()
    const interval = setInterval(fetchAlerts, 10000)
    return () => clearInterval(interval)
  }, [])
  
  const fetchAlerts = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/fraud/alerts`)
      setAlerts(response.data)
      setLoading(false)
    } catch (error) {
      console.error('Error fetching alerts:', error)
    }
  }
  
  const getRiskBadge = (level) => {
    const styles = {
      critical: 'bg-red-600 text-white',
      high: 'bg-red-100 text-red-800',
      medium: 'bg-yellow-100 text-yellow-800',
      low: 'bg-green-100 text-green-800'
    }
    return `px-2 py-1 rounded-full text-xs font-medium ${styles[level] || styles.low}`
  }
  
  if (loading) return <div className="text-center py-8">Loading alerts...</div>
  
  return (
    <div className="space-y-4">
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-2">Fraud Alert Feed</h2>
        <p className="text-gray-600 text-sm mb-4">Real-time fraud detection alerts from AI engine</p>
        
        {alerts.length === 0 ? (
          <div className="text-center py-8 text-gray-500">No fraud alerts detected</div>
        ) : (
          <div className="space-y-3">
            {alerts.map((alert) => (
              <div key={alert.id} className="border rounded-lg p-4 hover:shadow-md transition">
                <div className="flex justify-between items-start">
                  <div>
                    <div className="flex items-center space-x-2 mb-2">
                      <span className={getRiskBadge(alert.risk_level)}>{alert.risk_level.toUpperCase()}</span>
                      <span className="text-sm text-gray-500">{alert.alert_type.replace('_', ' ').toUpperCase()}</span>
                    </div>
                    <p className="font-medium">Phone: {alert.phone_number}</p>
                    {alert.ai_analysis && (
                      <>
                        <p className="text-sm text-gray-600 mt-1">{alert.ai_analysis.explanation}</p>
                        <p className="text-xs text-gray-400 mt-1">Action: {alert.action_taken}</p>
                      </>
                    )}
                  </div>
                  <div className="text-right">
                    <p className="text-xs text-gray-400">{new Date(alert.created_at).toLocaleString()}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default FraudAlertFeed