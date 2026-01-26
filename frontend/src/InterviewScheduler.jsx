import React, { useState, useEffect } from 'react';
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';
import { getProposals, createProposal, deleteProposal } from './api.js'; // APIをインポート

const InterviewScheduler = () => {
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [candidateDates, setCandidateDates] = useState([]); // データベースからのリスト
  const [timeSlot, setTimeSlot] = useState("10:00");
  const [loading, setLoading] = useState(false);

  // 初期読み込み：データベースから候補日を取得
  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const data = await getProposals();
      setCandidateDates(data);
    } catch (err) {
      console.error(err.message);
    }
  };

  // 候補日をデータベースに保存
  const addCandidate = async () => {
    const dateString = selectedDate.toLocaleDateString('ja-JP');
    const newEntry = `${dateString} ${timeSlot}`;
    
    // 重複チェック（表示上の重複を防ぐ）
    if (candidateDates.some(c => c.date_text === newEntry)) return;

    try {
      setLoading(true);
      await createProposal(newEntry);
      await fetchData(); // リストを再更新
    } catch (err) {
      alert("保存に失敗しました");
    } finally {
      setLoading(false);
    }
  };

  // 候補日をデータベースから削除
  const removeCandidate = async (id) => {
    try {
      await deleteProposal(id);
      await fetchData(); // リストを再更新
    } catch (err) {
      alert("削除に失敗しました");
    }
  };

  return (
    <div style={{ marginTop: '20px', padding: '20px', border: '1px solid #e5e7eb', borderRadius: '8px', backgroundColor: '#fff' }}>
      <div style={{ display: 'flex', gap: '20px', flexWrap: 'wrap' }}>
        <div>
          <Calendar onChange={setSelectedDate} value={selectedDate} locale="ja-JP" />
        </div>

        <div style={{ flex: 1 }}>
          <div style={{ marginBottom: '15px' }}>
            <p style={{ fontWeight: 'bold' }}>選択日: {selectedDate.toLocaleDateString('ja-JP')}</p>
            <input 
              type="time" 
              value={timeSlot} 
              onChange={(e) => setTimeSlot(e.target.value)}
              style={{ padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}
            />
            <button 
              type="button"
              onClick={addCandidate}
              disabled={loading}
              style={{ marginLeft: '10px', padding: '8px 15px', backgroundColor: '#10b981', color: 'white', border: 'none', borderRadius: '4px', cursor: loading ? 'not-allowed' : 'pointer' }}
            >
              {loading ? '保存中...' : '候補に追加'}
            </button>
          </div>

          <p style={{ fontWeight: 'bold' }}>保存済みの候補リスト:</p>
          <ul style={{ listStyle: 'none', padding: 0 }}>
            {candidateDates.length === 0 && <li style={{ color: '#9ca3af' }}>候補がありません</li>}
            {candidateDates.map((item) => (
              <li key={item.id} style={{ display: 'flex', justifyContent: 'space-between', padding: '8px', backgroundColor: '#f3f4f6', marginBottom: '4px', borderRadius: '4px' }}>
                {item.date_text}
                <button 
                  onClick={() => removeCandidate(item.id)}
                  style={{ color: '#ef4444', border: 'none', background: 'none', cursor: 'pointer' }}
                >
                  削除
                </button>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default InterviewScheduler;