import { useEffect, useState } from 'react'
import { QUESTIONS, SELF_ASSESSMENT_QUESTION } from './data/questions'
import { predict, contribute } from './api/client'
import { HeartIcon } from './components/Icons'
import Welcome from './components/Welcome'
import Questionnaire from './components/Questionnaire'
import Result from './components/Result'
import SurveyComplete from './components/SurveyComplete'
import Admin from './components/Admin'

const STAGE = {
  WELCOME: 'welcome',
  QUESTIONS: 'questions',
  RESULT: 'result',
}

// u režimu ankete pitanje o samoproceni ide PRVO, pa tek onda ostala
const SURVEY_QUESTIONS = [SELF_ASSESSMENT_QUESTION, ...QUESTIONS]

export default function App() {
  const [stage, setStage] = useState(STAGE.WELCOME)
  const [mode, setMode] = useState('predict')
  const [index, setIndex] = useState(0)
  const [answers, setAnswers] = useState({})
  const [result, setResult] = useState(null)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState(null)

  // rutiranje preko hash-a (#admin) - bez react-router biblioteke
  const [isAdmin, setIsAdmin] = useState(window.location.hash === '#admin')

  useEffect(() => {
    const onHashChange = () => setIsAdmin(window.location.hash === '#admin')
    window.addEventListener('hashchange', onHashChange)
    return () => window.removeEventListener('hashchange', onHashChange)
  }, [])

  const questions = mode === 'contribute' ? SURVEY_QUESTIONS : QUESTIONS

  function handleStart(selectedMode) {
    setMode(selectedMode)
    setAnswers({})
    setResult(null)
    setIndex(0)
    setError(null)
    setStage(STAGE.QUESTIONS)
  }

  function handleAnswer(questionId, value) {
    setAnswers((prev) => ({ ...prev, [questionId]: value }))
  }

  async function handleNext() {
    if (index < questions.length - 1) {
      setIndex(index + 1)
      return
    }

    setSubmitting(true)
    setError(null)
    try {
      const response = mode === 'contribute' ? await contribute(answers) : await predict(answers)
      setResult(response)
      setStage(STAGE.RESULT)
    } catch (err) {
      setError(
        'Unable to send your answers. Please check that the server is running ' +
          `(python -m uvicorn api.main:app --reload). Details: ${err.message}`
      )
    } finally {
      setSubmitting(false)
    }
  }

  function handleRestart() {
    setAnswers({})
    setResult(null)
    setIndex(0)
    setError(null)
    setStage(STAGE.WELCOME)
  }

  if (isAdmin) {
    return (
      <div className="app">
        <div className="shell">
          <header className="brand">
            <div className="brand__mark">
              <HeartIcon />
            </div>
            <div>
              <div className="brand__name">Postpartum Support</div>
              <div className="brand__sub">Administration</div>
            </div>
          </header>
          <Admin onExit={() => { window.location.hash = '' }} />
        </div>
      </div>
    )
  }

  return (
    <div className="app">
      <div className="shell">
        <header className="brand">
          <div className="brand__mark">
            <HeartIcon />
          </div>
          <div>
            <div className="brand__name">Postpartum Support</div>
            <div className="brand__sub">
              {stage === STAGE.QUESTIONS && mode === 'contribute'
                ? 'Collecting data for research'
                : 'Preliminary risk assessment'}
            </div>
          </div>
        </header>

        {error && <div className="error">{error}</div>}

        {submitting && (
          <div className="card state">
            <div className="spinner" />
            <div className="state__text">
              {mode === 'contribute' ? 'Saving your answers…' : 'Processing your answers…'}
            </div>
          </div>
        )}

        {!submitting && stage === STAGE.WELCOME && (
          <Welcome onStart={handleStart} questionCount={QUESTIONS.length} />
        )}

        {!submitting && stage === STAGE.QUESTIONS && (
          <Questionnaire
            questions={questions}
            index={index}
            answers={answers}
            onAnswer={handleAnswer}
            onBack={() => (index === 0 ? handleRestart() : setIndex(index - 1))}
            onNext={handleNext}
            submitting={submitting}
            finalLabel={mode === 'contribute' ? 'Submit answers' : 'Show result'}
          />
        )}

        {!submitting && stage === STAGE.RESULT && result && mode === 'predict' && (
          <Result result={result} answers={answers} onRestart={handleRestart} />
        )}

        {!submitting && stage === STAGE.RESULT && result && mode === 'contribute' && (
          <SurveyComplete result={result} onRestart={handleRestart} />
        )}

        <p className="disclaimer">
          This application was developed as part of a university thesis and is
          intended for informational purposes only. It does not constitute a
          medical diagnosis and does not replace advice, diagnosis, or treatment
          from a healthcare professional.
        </p>
      </div>
    </div>
  )
}
