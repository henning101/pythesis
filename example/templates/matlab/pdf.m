set(gca, "FontName", "Times New Roman");
ax = gca;
outerpos = ax.OuterPosition;
ti = ax.TightInset;
margin = 0.01
left = outerpos(1) + ti(1) + margin;
bottom = outerpos(2) + ti(2) + margin;
ax_width = outerpos(3) - ti(1) - ti(3) - margin * 2;
ax_height = outerpos(4) - ti(2) - ti(4) - margin * 2;
ax.Position = [left bottom ax_width ax_height];
fig = gcf;
fig.PaperPositionMode = "auto"
fig_pos = fig.PaperPosition;
fig.PaperSize = [fig_pos(3) fig_pos(4)];
fig.Renderer='Painters';
print(fig, "-dpdf", "{{pdfpath}}");
close all;
