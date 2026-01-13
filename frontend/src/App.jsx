#企業情報の入力フォームの作成
import { useEffect, useState } from 'react'

function App() {
  const [companies, setCompanies] = useState([])
  const [name, setName] = useState('')    // 入力用
  const [error, setError] = useState(null)

  // 企業一覧取得
  const fetchCompanies = () => {
    fetch('http://127.0.0.1:5000/api/companies')
      .then(res => {
        if (!res.ok) throw new Error('GET error')
        return res.json()
      })
      .then(data => setCompanies(data))
      .catch(err => setError(err.message))
  }

  useEffect(() => {
    fetchCompanies()
  }, [])

  // 企業追加
  const addCompany = (e) => {
    e.preventDefault()
    setError(null)

    fetch('http://127.0.0.1:5000/api/companies', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name })
    })
      .then(res => {
        if (!res.ok) throw new Error('POST error')
        return res.json()
      })
      .then(() => {
        setName('')         // 入力欄クリア
        fetchCompanies()    // 一覧更新
      })
      .catch(err => setError(err.message))
  }

  return (
    <div style={{ padding: '40px' }}>
      <h1>Companies</h1>

      <form onSubmit={addCompany}>
        <input
          value={name}
          onChange={e => setName(e.target.value)}
          placeholder="企業名"
        />
        <button type="submit">追加</button>
      </form>

      {error && <p style={{ color: 'red' }}>❌ {error}</p>}

      <ul>
        {companies.map(c => (
          <li key={c.id}>{c.name}</li>
        ))}
      </ul>
    </div>
  )
}

export default App
