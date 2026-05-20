package com.example.websitebackend.service;

import com.example.websitebackend.dto.InsightCreateRequest;
import com.example.websitebackend.dto.InsightUpdateRequest;
import com.example.websitebackend.model.Insight;
import com.example.websitebackend.repository.InsightRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class InsightService {

    private final InsightRepository insightRepository;

    public Page<Insight> getInsights(int skip, int limit) {
        int page = skip / limit;
        Pageable pageable = PageRequest.of(page, limit);
        return insightRepository.findAll(pageable);
    }

    public Insight createInsight(InsightCreateRequest request) {
        Insight insight = new Insight();
        insight.setPersonName(request.getPersonName());
        insight.setDescription(request.getDescription());
        insight.setImage(request.getImage());
        insight.setInstaLink(request.getInstaLink());

        // Apply custom styles if provided, otherwise the Entity defaults will remain
        if (request.getTitle() != null) insight.setTitle(request.getTitle());
        if (request.getBgColor() != null) insight.setBgColor(request.getBgColor());
        if (request.getBorderColor() != null) insight.setBorderColor(request.getBorderColor());
        if (request.getSize() != null) insight.setSize(request.getSize());
        if (request.getYear() != null) insight.setYear(request.getYear());

        return insightRepository.save(insight);
    }

    public Insight updateInsight(String id, InsightUpdateRequest request) {
        Insight insight = insightRepository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("Insight not found"));

        if (request.getPersonName() != null) insight.setPersonName(request.getPersonName());
        if (request.getDescription() != null) insight.setDescription(request.getDescription());
        if (request.getImage() != null) insight.setImage(request.getImage());
        if (request.getInstaLink() != null) insight.setInstaLink(request.getInstaLink());

        if (request.getTitle() != null) insight.setTitle(request.getTitle());
        if (request.getBgColor() != null) insight.setBgColor(request.getBgColor());
        if (request.getBorderColor() != null) insight.setBorderColor(request.getBorderColor());
        if (request.getSize() != null) insight.setSize(request.getSize());
        if (request.getYear() != null) insight.setYear(request.getYear());

        return insightRepository.save(insight);
    }

    public void deleteInsight(String id) {
        if (!insightRepository.existsById(id)) {
            throw new IllegalArgumentException("Insight not found");
        }
        insightRepository.deleteById(id);
    }
}