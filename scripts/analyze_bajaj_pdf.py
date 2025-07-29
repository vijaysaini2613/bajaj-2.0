# scripts/analyze_bajaj_pdf.py

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.document_processor import DocumentProcessor
import re

def analyze_bajaj_pdf():
    """Analyze the Bajaj PDF to understand its structure and content"""
    
    bajaj_pdf_path = r"c:\Users\saini\Downloads\BAJHLIP23020V012223.pdf"
    
    if not os.path.exists(bajaj_pdf_path):
        print(f"❌ PDF file not found: {bajaj_pdf_path}")
        return
    
    print("📄 Analyzing Bajaj Insurance Policy PDF...")
    print("=" * 60)
    
    try:
        # Extract text
        doc_processor = DocumentProcessor()
        text = doc_processor.extract_text(bajaj_pdf_path)
        
        print(f"📊 Document Statistics:")
        print(f"   - Total characters: {len(text):,}")
        print(f"   - Total words: {len(text.split()):,}")
        print(f"   - Total lines: {len(text.split(chr(10))):,}")
        
        # Find key sections
        print(f"\n🔍 Key Sections Found:")
        sections = [
            "EXCLUSIONS",
            "BENEFITS", 
            "CONDITIONS",
            "COVERAGE",
            "WAITING PERIOD",
            "PRE-EXISTING",
            "CLAIM",
            "PREMIUM",
            "MATERNITY",
            "DENTAL"
        ]
        
        text_upper = text.upper()
        for section in sections:
            count = text_upper.count(section)
            if count > 0:
                print(f"   ✅ {section}: {count} mentions")
        
        # Extract potential clauses
        print(f"\n📋 Sample Content Preview:")
        
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        relevant_sentences = []
        
        keywords = ['exclusion', 'coverage', 'benefit', 'waiting period', 'claim', 'condition']
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 50 and any(keyword.lower() in sentence.lower() for keyword in keywords):
                relevant_sentences.append(sentence)
                if len(relevant_sentences) >= 5:  # Show first 5 relevant sentences
                    break
        
        for i, sentence in enumerate(relevant_sentences, 1):
            print(f"\n{i}. {sentence[:200]}{'...' if len(sentence) > 200 else ''}")
        
        # Save extracted content for review
        output_file = "data/bajaj_pdf_analysis.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("BAJAJ INSURANCE POLICY - EXTRACTED TEXT\n")
            f.write("=" * 50 + "\n\n")
            f.write(text)
        
        print(f"\n💾 Full text saved to: {output_file}")
        print("\n✅ Analysis complete! Review the extracted content to identify policy clauses.")
        
    except Exception as e:
        print(f"❌ Error analyzing PDF: {e}")

if __name__ == "__main__":
    analyze_bajaj_pdf()
