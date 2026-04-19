import { useState } from "react";

export default function TagInput({ value = [], onChange }) {
  const [input, setInput] = useState("");

  const add = () => {
    const v = input.trim();
    if (v && !value.includes(v)) onChange([...value, v]);
    setInput("");
  };

  const remove = (t) => onChange(value.filter(x => x !== t));

  return (
    <div className="tag-input-wrap" onClick={() => {}}>
      {value.map(t => (
        <span key={t} className="tag tag-removable">
          {t}
          <button type="button" onClick={() => remove(t)}>x</button>
        </span>
      ))}
      <input
        value={input}
        onChange={e => setInput(e.target.value)}
        onKeyDown={e => { if (e.key === "Enter" || e.key === ",") { e.preventDefault(); add(); } }}
        placeholder={value.length === 0 ? "Escribe y presiona Enter..." : ""}
      />
    </div>
  );
}