import { ClockIcon, ShieldIcon, InfoIcon, ArrowRightIcon, GaugeIcon, DatabaseIcon } from './Icons'

export default function Welcome({ onStart, questionCount }) {
  return (
    <div className="card">
      <h1 className="hero__title">How are you feeling after giving birth?</h1>
      <p className="hero__lead">
        Choose what you would like to do. Both options are anonymous and take
        just a few minutes.
      </p>

      <div className="modes">
        <button className="mode" onClick={() => onStart('predict')} type="button">
          <div className="mode__icon mode__icon--primary">
            <GaugeIcon />
          </div>
          <div className="mode__body">
            <div className="mode__title">Assess my risk</div>
            <div className="mode__desc">
              Answer {questionCount} questions and get an approximate assessment of
              postpartum depression risk.
            </div>
          </div>
          <ArrowRightIcon />
        </button>

        <button className="mode" onClick={() => onStart('contribute')} type="button">
          <div className="mode__icon mode__icon--accent">
            <DatabaseIcon />
          </div>
          <div className="mode__body">
            <div className="mode__title">Contribute to research</div>
            <div className="mode__desc">
              Whether or not you feel depressed, your answers help make the
              assessment more accurate for other women.
            </div>
          </div>
          <ArrowRightIcon />
        </button>
      </div>

      <div className="facts">
        <div className="fact">
          <ClockIcon />
          <div className="fact__text">
            <strong>Quick, no sign-up</strong>
            <span>No account or contact information needed.</span>
          </div>
        </div>
        <div className="fact">
          <ShieldIcon />
          <div className="fact__text">
            <strong>Anonymous</strong>
            <span>No data that could identify you is stored.</span>
          </div>
        </div>
        <div className="fact">
          <InfoIcon />
          <div className="fact__text">
            <strong>Not a diagnosis</strong>
            <span>The result is indicative and does not replace a conversation with a doctor.</span>
          </div>
        </div>
      </div>
    </div>
  )
}
