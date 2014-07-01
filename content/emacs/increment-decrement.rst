Increment-Decrement for Emacs
=============================
:date: 2013-04-17
:category: programming
:tags: emacs, el-get
:author: Yusuke Tsutsumi

Here's a small increment/decrement function I wrote, because I like how vim has one:

.. code-block:: scheme

    ;; check if string is an integer
    (defun string-integer-p (string)
      (if (string-match "\\`[-+]?[0-9]+\\'" string)
          t
        nil))

    ;; Decrement Int
    (defun decrement ()
      "Decrement the integer that the cursor is on."
      (interactive)
      (let ((x (thing-at-point 'symbol)))
        (when (string-integer-p x)
          (let ((x-int (string-to-number x))
                (bds (bounds-of-thing-at-point 'symbol)))
            (progn
              (delete-region (car bds) (cdr bds))
              (insert (number-to-string (- x-int 1)))
            )
          )
        )
      )
    )

    ;; Increment Int
    (defun increment ()
      "Increment the integer that the cursor is on."
      (interactive)
      (let ((x (thing-at-point 'symbol)))
        (when (string-integer-p x)
          (let ((x-int (string-to-number x))
                (bds (bounds-of-thing-at-point 'symbol)))
            (progn
              (delete-region (car bds) (cdr bds))
              (insert (number-to-string (+ x-int 1)))
            )
          )
        )
      )
    )
