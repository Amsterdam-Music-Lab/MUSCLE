export const renderLabel = (label: string, size = "fa-lg") => {
    if (!label) return label
    if (label.startsWith('fa-')) return <span className={`fa-solid ${label} ${size}`}></span>
    else return label
}
