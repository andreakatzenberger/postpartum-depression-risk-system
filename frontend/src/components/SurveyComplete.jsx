import { AlertIcon, CheckIcon, RefreshIcon } from './Icons'

export default function SurveyComplete({ result, onRestart }) {
  return (
    <div className="card result">
      <div className="done">
        <CheckIcon />
      </div>

      <h2 className="verdict">Thank you</h2>
      <p className="result__lead">
        Your answers have been saved and will be used to improve the assessment
        for other women. No data that identifies you has been recorded.
      </p>

      {result.crisis_flag && (
        <div className="crisis">
          <AlertIcon />
          <div>
            <div className="crisis__title">Seek support</div>
            <div className="crisis__body">{result.crisis_message}</div>
          </div>
        </div>
      )}

      <div className="stats">
        <div className="stat">
          <div className="stat__num">{result.survey_records}</div>
          <div className="stat__cap">collected through the survey</div>
        </div>
        <div className="stat">
          <div className="stat__num">{result.total_records}</div>
          <div className="stat__cap">total in the dataset</div>
        </div>
      </div>

      <button className="btn btn--primary" onClick={onRestart} type="button">
        <RefreshIcon />
        Back to start
      </button>
    </div>
  )
}
