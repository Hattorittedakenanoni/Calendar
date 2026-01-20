// API通信をまとめるファイル

const API_BASE = 'http://127.0.0.1:5000/api';

// ========================================
// 企業（就活状況）API
// ========================================

// 企業一覧取得
export async function getCompanies() {
  const response = await fetch(`${API_BASE}/companies`);
  if (!response.ok) {
    throw new Error('企業一覧の取得に失敗しました');
  }
  return response.json();
}

// 企業追加
export async function createCompany(data) {
  const response = await fetch(`${API_BASE}/companies`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });
  if (!response.ok) {
    throw new Error('企業の追加に失敗しました');
  }
  return response.json();
}

// 企業更新
export async function updateCompany(companyId, data) {
  const response = await fetch(`${API_BASE}/companies/${companyId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });
  if (!response.ok) {
    throw new Error('企業情報の更新に失敗しました');
  }
  return response.json();
}

// 企業削除
export async function deleteCompany(companyId) {
  const response = await fetch(`${API_BASE}/companies/${companyId}`, {
    method: 'DELETE',
  });
  if (!response.ok) {
    throw new Error('企業の削除に失敗しました');
  }
  return response.json();
}

// ヘルスチェック
export async function healthCheck() {
  const response = await fetch(`${API_BASE}/health`);
  return response.json();
}