import axios from "axios"
import { useState } from "react"

type props = {
    setMessages: any
}

const Title = ({ setMessages}: props) => {
    const [isResetting, setIsResetting] = useState (false)
    const resetConversion = async () => {
        setIsResetting (true)

        await axios.get ("http://localhost:8000/reset-chats").then ((res) => {
            if (res.status == 200) {
                alert (res.data)
                setMessages ([])
            }else {
                console.error ("there was an error with the API Request")
            }
        }).catch ((err) => {
            console.error (err.message)
        })

        setIsResetting (false)
    }


    return <div className="flex justify-between w-full items-center p-4 bg-slate-700 text-white font-bold shadow">
        <div className="italic">Mira</div>
        <button onClick={resetConversion} className={"transition-all duration-300 text-blue-300 hover:text-pink-500 " + (isResetting && "animate-pulse")}>R</button>
    </div>
}

export default Title