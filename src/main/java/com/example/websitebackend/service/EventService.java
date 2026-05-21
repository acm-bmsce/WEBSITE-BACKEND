package com.example.websitebackend.service;

import com.example.websitebackend.dto.EventCreateRequest;
import com.example.websitebackend.dto.EventUpdateRequest;
import com.example.websitebackend.model.Event;
import com.example.websitebackend.repository.EventRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class EventService {

    private final EventRepository eventRepository;

    public Page<Event> getEvents(int skip, int limit, Boolean featured) {
        // Spring uses PageRequest(page_number, size) instead of skip/limit
        int page = skip / limit;
        Pageable pageable = PageRequest.of(page, limit, Sort.by(Sort.Direction.DESC, "date"));

        if (featured != null) {
            return eventRepository.findByFeatured(featured, pageable); // ✅ Changed to match Event model (featured)
        }
        return eventRepository.findAll(pageable);
    }

    public Event createEvent(EventCreateRequest request) {
        Event event = new Event();
        event.setTitle(request.getTitle());
        event.setDescription(request.getDescription());

        // ✅ Direct transfer! No more manual String parsing required
        event.setDate(request.getDate());

        event.setImage(request.getImage());
        event.setFullDescription(request.getFullDescription());
        event.setOutcomes(request.getOutcomes());
        if (request.getGallery() != null) event.setGallery(request.getGallery());
        event.setLocation(request.getLocation());

        // ✅ Direct transfer! No more try/catch for Integer parsing
        if (request.getAttendees() != null) {
            event.setAttendees(request.getAttendees());
        }

        event.setRegistrationLink(request.getRegistrationLink());
        event.setFeatured(request.isFeatured());

        return eventRepository.save(event);
    }

    public Event updateEvent(String eventId, EventUpdateRequest request) {
        Event event = eventRepository.findById(eventId)
                .orElseThrow(() -> new IllegalArgumentException("Event not found"));

        if (request.getTitle() != null) event.setTitle(request.getTitle());
        if (request.getDescription() != null) event.setDescription(request.getDescription());

        // ✅ Direct transfer! No more manual String parsing required
        if (request.getDate() != null) {
            event.setDate(request.getDate());
        }

        if (request.getImage() != null) event.setImage(request.getImage());
        if (request.getFullDescription() != null) event.setFullDescription(request.getFullDescription());
        if (request.getOutcomes() != null) event.setOutcomes(request.getOutcomes());
        if (request.getGallery() != null) event.setGallery(request.getGallery());
        if (request.getLocation() != null) event.setLocation(request.getLocation());
        if (request.getAttendees() != null) event.setAttendees(request.getAttendees());
        if (request.getRegistrationLink() != null) event.setRegistrationLink(request.getRegistrationLink());

        // ✅ Assuming your UpdateRequest DTO uses 'isFeatured' (Boolean)
        if (request.getIsFeatured() != null) event.setFeatured(request.getIsFeatured());

        return eventRepository.save(event);
    }

    public void deleteEvent(String eventId) {
        if (!eventRepository.existsById(eventId)) {
            throw new IllegalArgumentException("Event not found");
        }
        eventRepository.deleteById(eventId);
    }
}