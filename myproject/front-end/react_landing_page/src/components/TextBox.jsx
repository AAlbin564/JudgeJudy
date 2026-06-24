import style from '../styles/textBox.module.css'

export default function TextBox({ reply, setReply }) {
    return (
           <textarea className={style.textBox} value={reply} onChange={(e) => setReply(e.target.value)}>
           </textarea>

    )
}