import style from '../styles/textBox.module.css'

export default function TextBox({}) {
    return (
           <textarea className={style.textBox}>
            This is my favorite text box
           </textarea>

    )
}