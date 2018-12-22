Sub alphabetical_testing()

    Dim volume As Double
    Dim ticker As Double
    
    For Each ws In Worksheets

    If ActiveSheet.Index = Worksheets.Count Then
    Worksheets(1).Select
    Else
    ActiveSheet.Next.Select
    End If


        ticker = 2
        Range("I1").Value = "Ticker Symbol"
        Range("J1").Value = "Total Volume"
    
        Dim totalrows As Double
        totalrows = Cells(Rows.Count, "A").End(xlUp).Row
    
        For r = 2 To totalrows
    
            If Cells(r, 1).Value <> Cells(r + 1, 1).Value Then
                volume = volume + Cells(r, 7).Value
                Range("I" & ticker).Value = Cells(r, 1).Value
                Range("J" & ticker).Value = volume
                ticker = ticker + 1
                volume = 0
            
            Else
                volume = volume + Cells(r, 7).Value
        
            End If
        
        Next
            
    Next

End Sub


