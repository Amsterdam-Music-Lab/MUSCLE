import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

export const renderLabel = (label, size="1x") => {
    if (label.startsWith('ti-')) return <span className={label}></span>
    if (label.startsWith('fa-')) return <FontAwesomeIcon icon={label.substring(3)} size={size}/>
    else return label
}
