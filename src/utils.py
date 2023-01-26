def remove_commas(text: str) -> str:
    '''
    Remove the commas from the text
    
    params:
        text: Text to remove the commas from
        
    returns:
        text: Text without commas, newlines, tabs, etc.
    '''
    text = text.replace('\n', ' ')
    text = text.replace('\r', ' ')
    text = text.replace('\t', ' ')
    text = text.replace('\xa0', ' ')
    text = text.replace(',', ' ')
    text = text.replace(',', '')
    return text

