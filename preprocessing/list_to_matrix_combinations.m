%% prepare list of all pairs from list of labels
in=fopen('raw_1000_ImageNet_categories.txt','r');

i=0;
while 1
    tline=fgetl(in);
    if ~ischar(tline), break, end
    %disp(tline)
    i=i+1;
    lines{i}=tline;
end
fclose(in);

out=fopen('all_permutations_labels.txt','w');
for i=1:length(lines)
    for j=1:length(lines)
        fprintf(out,'%s\n',lines{i});
        fprintf(out,'%s\n',lines{j});
    end
end
fclose(out);

%% calculate distance for each pair using the GoogleNews dataset
%./distance2 ./data/GoogleNews-vectors-negative300.bin  < all_permutations_labels.txt >vystup.txt

%% create matrix from outputs
r=csvread('vystup.txt');
r=reshape(r,1000,1000);
