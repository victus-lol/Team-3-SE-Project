import { useEffect, useRef } from 'react'

/** Keep keyboard focus inside an open dialog and return it to its opener. */
export default function useDialogAccessibility(dialogRef, isOpen, onClose) {
  const onCloseRef = useRef(onClose)

  useEffect(() => {
    onCloseRef.current = onClose
  }, [onClose])

  useEffect(() => {
    const dialog = dialogRef.current
    if (!isOpen || !dialog) return undefined

    const previouslyFocused = document.activeElement
    const focusableSelector = 'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'
    const getFocusable = () => [...dialog.querySelectorAll(focusableSelector)]
      .filter((element) => element.getAttribute('aria-hidden') !== 'true')

    const focusable = getFocusable()
    const initialFocus = dialog.querySelector('[data-dialog-autofocus]') || focusable[0] || dialog
    initialFocus.focus()

    const handleKeyDown = (event) => {
      if (event.key === 'Escape') {
        event.preventDefault()
        onCloseRef.current?.()
        return
      }

      if (event.key !== 'Tab') return
      const items = getFocusable()
      if (items.length === 0) {
        event.preventDefault()
        dialog.focus()
      } else if (event.shiftKey && document.activeElement === items[0]) {
        event.preventDefault()
        items.at(-1).focus()
      } else if (!event.shiftKey && document.activeElement === items.at(-1)) {
        event.preventDefault()
        items[0].focus()
      }
    }

    dialog.addEventListener('keydown', handleKeyDown)
    return () => {
      dialog.removeEventListener('keydown', handleKeyDown)
      if (previouslyFocused instanceof HTMLElement && previouslyFocused.isConnected) {
        previouslyFocused.focus()
      }
    }
  }, [dialogRef, isOpen])
}
