import { useEffect, useState } from 'react'
import { QUESTIONS } from '../data/questions'
import { AlertIcon, RefreshIcon } from './Icons'

const RADIUS = 84
const CIRCUMFERENCE = 2 * Math.PI * RADIUS

function riskLevel(probability) {
  if (probability < 0.4) {
    return {
      color: 'var(--risk-low)',
      title: 'Low indicators',
      lead: 'Your answers do not indicate significant signs of postpartum depression. If you are still not feeling well, talk to a doctor regardless of this result.',
    }
  }
  if (probability < 0.7) {
    return {
      color: 'var(--risk-mid)',
      title: 'Moderate indicators',
      lead: 'Your answers indicate some signs worth paying attention to. Talking with a doctor or psychologist can help get a clearer picture.',
    }
  }
  return {
    color: 'var(--risk-high)',
    title: 'Elevated indicators',
    lead: 'Your answers indicate several signs associated with postpartum depression. We recommend reaching out to a doctor or psychologist.',
  }
}

function answerLabel(questionId, value) {
  const question = QUESTIONS.find((q) => q.id === questionId)
  return question?.options.find((o) => o.value === value)?.label ?? value
}

export default function Result({ result, answers, onRestart }) {
  const [animatedOffset, setAnimatedOffset] = useState(CIRCUMFERENCE)
  const percentage = Math.round(result.predicted_probability * 100)
  const level = riskLevel(result.predicted_probability)

  useEffect(() => {
    const timer = setTimeout(() => {
      setAnimatedOffset(CIRCUMFERENCE * (1 - result.predicted_probability))
    }, 90)
    return () => clearTimeout(timer)
  }, [result.predicted_probability])

  return (
    <div className="card result">
      <div className="gauge">
        <svg width="190" height="190" viewBox="0 0 190 190">
          <circle className="gauge__track" cx="95" cy="95" r={RADIUS} fill="none" strokeWidth="13" />
          <circle
            className="gauge__value"
            cx="95"
            cy="95"
            r={RADIUS}
            fill="none"
            strokeWidth="13"
            stroke={level.color}
            strokeDasharray={CIRCUMFERENCE}
            strokeDashoffset={animatedOffset}
          />
        </svg>
        <div className="gauge__center">
          <div className="gauge__pct" style={{ color: level.color }}>
            {percentage}%
          </div>
          <div className="gauge__cap">estimate</div>
        </div>
      </div>

      <h2 className="verdict" style={{ color: level.color }}>
        {level.title}
      </h2>
      <p className="result__lead">{level.lead}</p>

      {result.crisis_flag && (
        <div className="crisis">
          <AlertIcon />
          <div>
            <div className="crisis__title">Seek support</div>
            <div className="crisis__body">{result.crisis_message}</div>
          </div>
        </div>
      )}

      <div className="breakdown">
        <div className="breakdown__title">Your answers</div>
        {QUESTIONS.map((question) => (
          <div className="answer-row" key={question.id}>
            <span className="answer-row__q">{question.label}</span>
            <span className="answer-row__a">{answerLabel(question.id, answers[question.id])}</span>
          </div>
        ))}
      </div>

      <button className="btn btn--primary" onClick={onRestart} type="button">
        <RefreshIcon />
        Retake the assessment
      </button>
    </div>
  )
}
