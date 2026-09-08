import { useState } from 'react'
import { adminLogin, adminOverview, adminRetrain } from '../api/client'
import { RefreshIcon, ArrowLeftIcon } from './Icons'

const RETRAIN_THRESHOLD = 100

function Metric({ label, value, hint }) {
  return (
    <div className="metric">
      <div className="metric__label">{label}</div>
      <div className="metric__value">{value}</div>
      {hint && <div className="metric__hint">{hint}</div>}
    </div>
  )
}

export default function Admin({ onExit }) {
  const [password, setPassword] = useState('')
  const [authed, setAuthed] = useState(false)
  const [overview, setOverview] = useState(null)
  const [retrainResult, setRetrainResult] = useState(null)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState(null)

  async function handleLogin(event) {
    event.preventDefault()
    setBusy(true)
    setError(null)
    try {
      await adminLogin(password)
      const data = await adminOverview(password)
      setOverview(data)
      setAuthed(true)
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  async function handleRetrain() {
    setBusy(true)
    setError(null)
    setRetrainResult(null)
    try {
      const result = await adminRetrain(password)
      setRetrainResult(result)
      setOverview(await adminOverview(password))
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  if (!authed) {
    return (
      <div className="card">
        <h1 className="hero__title">Administration</h1>
        <p className="hero__lead">Enter the password to access the overview and retrain the model.</p>

        {error && <div className="error">{error}</div>}

        <form onSubmit={handleLogin}>
          <input
            className="input"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password"
            autoFocus
          />
          <button className="btn btn--primary" type="submit" disabled={busy || !password}>
            {busy ? 'Checking…' : 'Log in'}
          </button>
        </form>

        <button className="btn btn--ghost admin__back" onClick={onExit} type="button">
          <ArrowLeftIcon />
          Back to app
        </button>
      </div>
    )
  }

  const { dataset, model, usage, new_rows_since_training: newRows } = overview
  const canRetrain = newRows >= RETRAIN_THRESHOLD

  return (
    <div className="card">
      <div className="admin__head">
        <h1 className="hero__title">Administration</h1>
        <span className="badge">{model.version}</span>
      </div>

      {error && <div className="error">{error}</div>}

      <div className="admin__section">Dataset</div>
      <div className="metrics">
        <Metric label="Total records" value={dataset.total} />
        <Metric label="From survey" value={dataset.anketa} hint={`${dataset.anketa_depresivnih} feeling depressed`} />
        <Metric label="Kaggle (imported)" value={dataset.kaggle} />
        <Metric
          label="New since training"
          value={newRows}
          hint={canRetrain ? 'Enough for retraining' : `Threshold: ${RETRAIN_THRESHOLD}`}
        />
      </div>

      <div className="admin__section">Active model</div>
      <div className="metrics">
        <Metric label="AUC" value={model.metrics?.auc ?? '—'} />
        <Metric label="Accuracy" value={model.metrics?.accuracy ?? '—'} />
        <Metric label="F1" value={model.metrics?.f1 ?? '—'} />
        <Metric label="Trained on" value={model.rows_at_training} hint="records" />
      </div>
      {model.trained_at && (
        <div className="admin__note">Last trained: {model.trained_at.replace('T', ' ')}</div>
      )}

      <div className="admin__section">Usage</div>
      <div className="metrics">
        <Metric label="Predictions made" value={usage.predictions_made} />
        <Metric
          label="Average prediction"
          value={usage.avg_predicted_probability ?? '—'}
          hint={usage.avg_predicted_probability > 0.7 ? 'High — check the model' : null}
        />
      </div>

      {retrainResult && (
        <div className={`retrain ${retrainResult.promoted ? 'retrain--ok' : 'retrain--skip'}`}>
          <div className="retrain__title">
            {retrainResult.promoted ? 'Model replaced' : 'Model not replaced'}
          </div>
          <div className="retrain__body">{retrainResult.reason}</div>
          <div className="retrain__compare">
            <div>
              <span>Old AUC</span>
              <strong>{retrainResult.champion?.auc ?? '—'}</strong>
            </div>
            <div>
              <span>New AUC</span>
              <strong>{retrainResult.challenger?.auc ?? '—'}</strong>
            </div>
          </div>
        </div>
      )}

      <button className="btn btn--primary admin__retrain" onClick={handleRetrain} disabled={busy} type="button">
        <RefreshIcon />
        {busy ? 'Training in progress…' : 'Retrain model'}
      </button>
      <div className="admin__note admin__note--center">
        The new model replaces the current one only if it performs better on the same test set.
      </div>

      <button className="btn btn--ghost admin__back" onClick={onExit} type="button">
        <ArrowLeftIcon />
        Back to app
      </button>
    </div>
  )
}
