/**
 * Adresa backenda se izvodi iz adrese sa koje je stranica učitana.
 *
 * Zašto ne fiksno 127.0.0.1: kad se aplikacija otvori na telefonu preko
 * mrežne adrese (npr. http://192.168.1.5:5173), "127.0.0.1" bi za telefon
 * značilo sam telefon, pa bi svi pozivi pukli. Ovako se automatski koristi
 * ista adresa računara na kojem radi i backend.
 */
const API_URL =
  import.meta.env.VITE_API_URL || `http://${window.location.hostname}:8000`

async function post(path, payload) {
  const response = await fetch(`${API_URL}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })

  if (!response.ok) {
    let detail = `Error ${response.status}`
    try {
      const body = await response.json()
      if (body.detail) detail = JSON.stringify(body.detail)
    } catch {
      // odgovor nije JSON - ostavljamo generičku poruku
    }
    throw new Error(detail)
  }

  return response.json()
}

/** Procena rizika - poziva model, ne menja skup podataka. */
export function predict(answers) {
  return post('/predict', answers)
}

/** Doprinos podataka - upisuje se u skup za treniranje, bez predikcije. */
export function contribute(answers) {
  return post('/contribute', answers)
}

/* ---------- admin ---------- */

async function adminRequest(path, password, method = 'GET') {
  const response = await fetch(`${API_URL}/admin${path}`, {
    method,
    headers: { 'X-Admin-Password': password },
  })

  if (response.status === 401) {
    throw new Error('Invalid password.')
  }
  if (!response.ok) {
    throw new Error(`Error ${response.status}`)
  }
  return response.json()
}

export function adminLogin(password) {
  return adminRequest('/login', password, 'POST')
}

export function adminOverview(password) {
  return adminRequest('/overview', password)
}

export function adminRetrain(password) {
  return adminRequest('/retrain', password, 'POST')
}
