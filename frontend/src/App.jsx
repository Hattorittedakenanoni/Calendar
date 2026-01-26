import { useEffect, useState } from 'react'
import { getCompanies, createCompany } from './api.js'
// �? カレンダーコンポ�?�ネントをインポ�?��?
import InterviewScheduler from './InterviewScheduler.jsx'

// 選�?ス�?ータスの選択肢
const STATUS_OPTIONS = ['応募中', '書類選�?中', '面接予�?', '�?�?', '不採用', '辞退']

// 志望度の選択肢
const LEVEL_OPTIONS = ['A', 'B', 'C']

function App() {
  const [companies, setCompanies] = useState([]) //companies:企業の�?ータ
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(true)

  // フォー�?の状�?
  const [formData, setFormData] = useState({
    company_name: '',
    via: '',
    status: '',
    level: '',
    start_time: '',
    end_time: '',
    goodpoint: '',
    badpoint: '',
    memo: '',
  })

  // 企業一覧取�?(backend(�?ータベ�?�ス)から�?報を得られる)
  const fetchCompanies = async () => {
    try {
      setLoading(true)
      const data = await getCompanies()
      setCompanies(data)
      setError(null)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchCompanies()
  }, [])

  // フォー�?入力�?�処�?
  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
  }

  // フォー�?リセ�?�?
  const resetForm = () => {
    setFormData({
      company_name: '',
      via: '',
      status: '',
      level: '',
      start_time: '',
      end_time: '',
      goodpoint: '',
      badpoint: '',
      memo: '',
    })
  }

  // 企業追�?
  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)

    if (!formData.company_name.trim()) {
      setError('企業名を入力してください')
      return
    }

    try {
      await createCompany(formData)
      resetForm()
      fetchCompanies()
    } catch (err) {
      setError(err.message)
    }
  }

  // 日時フォーマッ�?
  const formatDateTime = (isoString) => {
    if (!isoString) return '-'
    return new Date(isoString).toLocaleString('ja-JP', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    })
  }
  
  return (
    <div style={{ padding: '40px', maxWidth: '1200px', margin: '0 auto' }}>
      <h1>就活管�?アプリ</h1>

      {/* エラー表示 */}
      {error && (
        <p style={{ color: 'red', padding: '10px', backgroundColor: '#fee2e2', borderRadius: '4px' }}>
          {error}
        </p>
      )}

      {/* 入力フォー�? */}
      <div style={{ backgroundColor: '#f9fafb', padding: '20px', borderRadius: '8px', marginBottom: '20px' }}>
        <h2>企業を追�?</h2>
        <form onSubmit={handleSubmit}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
            {/* 企業�? */}
            <div>
              <label style={{ display: 'block', marginBottom: '4px', fontWeight: 'bold' }}>
                企業�? *
              </label>
              <input
                type="text"
                name="company_name"
                value={formData.company_name}
                onChange={handleChange}
                placeholder="�?: 株式会社�?�?"
                style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc', boxSizing: 'border-box' }}
                required
              />
            </div>

            {/* 経由 */}
            <div>
              <label style={{ display: 'block', marginBottom: '4px', fontWeight: 'bold' }}>
                経由
              </label>
              <input
                type="text"
                name="via"
                value={formData.via}
                onChange={handleChange}
                placeholder="�?: マイナビ、リクナビ"
                style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc', boxSizing: 'border-box' }}
              />
            </div>

            {/* 選�?ス�?ータス */}
            <div>
              <label style={{ display: 'block', marginBottom: '4px', fontWeight: 'bold' }}>
                選�?ス�?ータス
              </label>
              <select
                name="status"
                value={formData.status}
                onChange={handleChange}
                style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc', boxSizing: 'border-box' }}
              >
                <option value="">選択してください</option>
                {STATUS_OPTIONS.map(option => (
                  <option key={option} value={option}>{option}</option>
                ))}
              </select>
            </div>

            {/* 志望度 */}
            <div>
              <label style={{ display: 'block', marginBottom: '4px', fontWeight: 'bold' }}>
                志望度
              </label>
              <select
                name="level"
                value={formData.level}
                onChange={handleChange}
                style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc', boxSizing: 'border-box' }}
              >
                <option value="">選択してください</option>
                {LEVEL_OPTIONS.map(option => (
                  <option key={option} value={option}>{option}</option>
                ))}
              </select>
            </div>

            {/* 面接日時（開始�? */}
            <div>
              <label style={{ display: 'block', marginBottom: '4px', fontWeight: 'bold' }}>
                面接日時（開始�?
              </label>
              <input
                type="datetime-local"
                name="start_time"
                value={formData.start_time}
                onChange={handleChange}
                style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc', boxSizing: 'border-box' }}
              />
            </div>

            {/* 面接日時（終�??�? */}
            <div>
              <label style={{ display: 'block', marginBottom: '4px', fontWeight: 'bold' }}>
                面接日時（終�??�?
              </label>
              <input
                type="datetime-local"
                name="end_time"
                value={formData.end_time}
                onChange={handleChange}
                style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc', boxSizing: 'border-box' }}
              />
            </div>

            {/* 良�?と思う点 */}
            <div>
              <label style={{ display: 'block', marginBottom: '4px', fontWeight: 'bold' }}>
                良�?と思う点
              </label>
              <textarea
                name="goodpoint"
                value={formData.goodpoint}
                onChange={handleChange}
                style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc', minHeight: '60px', boxSizing: 'border-box' }}
              />
            </div>

            {/* 懸念点 */}
            <div>
              <label style={{ display: 'block', marginBottom: '4px', fontWeight: 'bold' }}>
                懸念点
              </label>
              <textarea
                name="badpoint"
                value={formData.badpoint}
                onChange={handleChange}
                style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc', minHeight: '60px', boxSizing: 'border-box' }}
              />
            </div>

            {/* メモ */}
            <div style={{ gridColumn: '1 / -1' }}>
              <label style={{ display: 'block', marginBottom: '4px', fontWeight: 'bold' }}>
                メモ
              </label>
              <textarea
                name="memo"
                value={formData.memo}
                onChange={handleChange}
                style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc', minHeight: '60px', boxSizing: 'border-box' }}
              />
            </div>

            {/* �? 追�??��面接候補日管�?コンポ�?�ネン�? */}
            <div style={{ gridColumn: '1 / -1' }}>
              <InterviewScheduler />
            </div>
          </div>

          <button
            type="submit"
            style={{
              marginTop: '16px',
              padding: '10px 20px',
              backgroundColor: '#2563eb',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            追�?
          </button>
        </form>
      </div>

      {/* 企業一覧 */}
      <div>
        <h2>応募企業一覧</h2>
        {loading ? (
          <p>読み込み中...</p>
        ) : companies.length === 0 ? (
          <p>ま�?企業が登録されて�?ません�?</p>
        ) : (
          <table style={{ width: '100%', borderCollapse: 'collapse', backgroundColor: 'white' }}>
            <thead>
              <tr style={{ backgroundColor: '#f9fafb' }}>
                <th style={{ padding: '12px', textAlign: 'left', borderBottom: '1px solid #e5e7eb' }}>企業�?</th>
                <th style={{ padding: '12px', textAlign: 'left', borderBottom: '1px solid #e5e7eb' }}>経由</th>
                <th style={{ padding: '12px', textAlign: 'left', borderBottom: '1px solid #e5e7eb' }}>ス�?ータス</th>
                <th style={{ padding: '12px', textAlign: 'left', borderBottom: '1px solid #e5e7eb' }}>志望度</th>
                <th style={{ padding: '12px', textAlign: 'left', borderBottom: '1px solid #e5e7eb' }}>面接日�?</th>
                <th style={{ padding: '12px', textAlign: 'left', borderBottom: '1px solid #e5e7eb' }}>良�?点</th>
                <th style={{ padding: '12px', textAlign: 'left', borderBottom: '1px solid #e5e7eb' }}>懸念点</th>
              </tr>
            </thead>
            <tbody>
              {companies.map(company => (
                <tr key={company.company_id} style={{ borderBottom: '1px solid #e5e7eb' }}>
                  <td style={{ padding: '12px' }}>{company.company_name}</td>
                  <td style={{ padding: '12px' }}>{company.via || '-'}</td>
                  <td style={{ padding: '12px' }}>{company.status || '-'}</td>
                  <td style={{ padding: '12px' }}>{company.level || '-'}</td>
                  <td style={{ padding: '12px' }}>{formatDateTime(company.start_time)}</td>
                  <td style={{ padding: '12px' }}>{company.goodpoint || '-'}</td>
                  <td style={{ padding: '12px' }}>{company.badpoint || '-'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

export default App