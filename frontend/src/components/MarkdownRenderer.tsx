import React from 'react';

interface MarkdownRendererProps {
  content: string;
  className?: string;
}

export const MarkdownRenderer: React.FC<MarkdownRendererProps> = ({ content, className = '' }) => {
  if (!content) return null;

  // Format inline markdown (bold, italic, inline code)
  const renderInline = (text: string) => {
    // Split by code tags first
    const codeParts = text.split(/(`[^`]+`)/g);

    return codeParts.map((part, pIdx) => {
      if (part.startsWith('`') && part.endsWith('`') && part.length > 2) {
        return (
          <code key={pIdx} className="px-1.5 py-0.5 rounded bg-slate-800 text-sky-300 font-mono text-[11px] border border-slate-700/60">
            {part.slice(1, -1)}
          </code>
        );
      }

      // Split by bold (**text**)
      const boldParts = part.split(/(\*\*[^*]+\*\*)/g);
      return boldParts.map((bPart, bIdx) => {
        if (bPart.startsWith('**') && bPart.endsWith('**') && bPart.length > 4) {
          return (
            <strong key={`${pIdx}-${bIdx}`} className="font-semibold text-white">
              {bPart.slice(2, -2)}
            </strong>
          );
        }

        // Split by italic (*text*)
        const italicParts = bPart.split(/(\*[^*]+\*)/g);
        return italicParts.map((iPart, iIdx) => {
          if (iPart.startsWith('*') && iPart.endsWith('*') && iPart.length > 2) {
            return (
              <em key={`${pIdx}-${bIdx}-${iIdx}`} className="italic text-slate-300">
                {iPart.slice(1, -1)}
              </em>
            );
          }
          return iPart;
        });
      });
    });
  };

  // Parse lines into block-level elements
  const lines = content.split('\n');
  const elements: React.ReactNode[] = [];
  let currentList: { type: 'ul' | 'ol'; items: string[] } | null = null;

  const flushList = () => {
    if (!currentList) return;
    if (currentList.type === 'ul') {
      elements.push(
        <ul key={`list-${elements.length}`} className="list-disc pl-5 space-y-1 my-1.5 text-slate-200">
          {currentList.items.map((item, idx) => (
            <li key={idx} className="leading-relaxed">
              {renderInline(item)}
            </li>
          ))}
        </ul>
      );
    } else {
      elements.push(
        <ol key={`list-${elements.length}`} className="list-decimal pl-5 space-y-1 my-1.5 text-slate-200">
          {currentList.items.map((item, idx) => (
            <li key={idx} className="leading-relaxed">
              {renderInline(item)}
            </li>
          ))}
        </ol>
      );
    }
    currentList = null;
  };

  for (let i = 0; i < lines.length; i++) {
    const rawLine = lines[i];
    const trimmed = rawLine.trim();

    if (!trimmed) {
      flushList();
      continue;
    }

    // Headings
    if (trimmed.startsWith('### ')) {
      flushList();
      elements.push(
        <h3 key={i} className="text-xs font-bold text-sky-300 uppercase tracking-wide mt-3 mb-1">
          {renderInline(trimmed.slice(4))}
        </h3>
      );
      continue;
    }

    if (trimmed.startsWith('## ')) {
      flushList();
      elements.push(
        <h2 key={i} className="text-sm font-bold text-white mt-3.5 mb-1.5 border-b border-slate-800 pb-1">
          {renderInline(trimmed.slice(3))}
        </h2>
      );
      continue;
    }

    if (trimmed.startsWith('# ')) {
      flushList();
      elements.push(
        <h1 key={i} className="text-base font-extrabold text-white mt-4 mb-2">
          {renderInline(trimmed.slice(2))}
        </h1>
      );
      continue;
    }

    // Blockquotes
    if (trimmed.startsWith('> ')) {
      flushList();
      elements.push(
        <blockquote key={i} className="border-l-2 border-sky-400 bg-sky-950/20 px-3 py-1.5 my-1.5 rounded-r text-slate-300 text-xs italic">
          {renderInline(trimmed.slice(2))}
        </blockquote>
      );
      continue;
    }

    // Horizontal Rule
    if (trimmed === '---' || trimmed === '***') {
      flushList();
      elements.push(<hr key={i} className="border-slate-800 my-2.5" />);
      continue;
    }

    // Unordered List Items (- or *)
    const ulMatch = trimmed.match(/^[-*]\s+(.+)/);
    if (ulMatch) {
      if (!currentList || currentList.type !== 'ul') {
        flushList();
        currentList = { type: 'ul', items: [] };
      }
      currentList.items.push(ulMatch[1]);
      continue;
    }

    // Ordered List Items (1. )
    const olMatch = trimmed.match(/^(\d+)\.\s+(.+)/);
    if (olMatch) {
      if (!currentList || currentList.type !== 'ol') {
        flushList();
        currentList = { type: 'ol', items: [] };
      }
      currentList.items.push(olMatch[2]);
      continue;
    }

    // Normal Paragraph
    flushList();
    elements.push(
      <p key={i} className="my-1 text-slate-200 leading-relaxed text-xs">
        {renderInline(trimmed)}
      </p>
    );
  }

  flushList();

  return <div className={`markdown-content space-y-1 ${className}`}>{elements}</div>;
};
