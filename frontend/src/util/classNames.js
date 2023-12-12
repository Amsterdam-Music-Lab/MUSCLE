/**
 *
 * @param  {...string} classes
 * @returns string
 */
export function classNames(...classes) {
    return classes.filter(Boolean).join(' ')
}

export default classNames
