from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Pet


class PetSerializer(serializers.ModelSerializer):
    """
    Serializer for Pet model.
    Used for creating and updating pets.
    """
    owner_email = serializers.EmailField(source='owner.email', read_only=True)
    owner_name = serializers.SerializerMethodField()
    age = serializers.IntegerField(
        required=False,
        allow_null=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(50)
        ],
        help_text='Pet age in years'
    )
    weight = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        required=False,
        allow_null=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(1000)
        ],
        help_text='Pet weight in kg'
    )

    class Meta:
        model = Pet
        fields = [
            'id',
            'owner',
            'owner_email',
            'owner_name',
            'name',
            'breed',
            'age',
            'weight',
            'gender',
            'pet_type',
            'date_of_birth',
            'color',
            'profile_picture',
            'microchip_number',
            'notes',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'owner_email',
            'owner_name',
            'created_at',
            'updated_at',
        ]

    def get_owner_name(self, obj):
        """
        Return owner's full name.
        """
        return obj.owner.get_full_name()

    def validate_name(self, value):
        """
        Validate pet name.
        """
        if not value or not value.strip():
            raise serializers.ValidationError(_('Pet name cannot be empty.'))
        return value.strip()

    def validate_microchip_number(self, value):
        """
        Validate microchip number uniqueness if provided.
        """
        if value:
            value = value.strip().upper()
            queryset = Pet.all_objects.filter(microchip_number=value)
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.exists():
                raise serializers.ValidationError(
                    _('A pet with this microchip number already exists.')
                )
        return value

    def validate(self, attrs):
        """
        Validate age and date_of_birth consistency.
        """
        age = attrs.get('age')
        date_of_birth = attrs.get('date_of_birth')
        
        if date_of_birth and age:
            from django.utils import timezone
            today = timezone.now().date()
            calculated_age = (today - date_of_birth).days // 365
            if abs(calculated_age - age) > 1:
                raise serializers.ValidationError({
                    'age': _('Age does not match date of birth. Please verify.')
                })
        
        return attrs

    def create(self, validated_data):
        """
        Create pet and set owner to current user if not provided.
        """
        request = self.context.get('request')
        if request and not validated_data.get('owner'):
            validated_data['owner'] = request.user
        return super().create(validated_data)


class PetListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing pets (minimal information).
    """
    owner_name = serializers.SerializerMethodField()

    class Meta:
        model = Pet
        fields = [
            'id',
            'name',
            'breed',
            'age',
            'weight',
            'gender',
            'pet_type',
            'owner_name',
            'profile_picture',
            'created_at',
        ]

    def get_owner_name(self, obj):
        """
        Return owner's full name.
        """
        return obj.owner.get_full_name()


class PetDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for pet detail view.
    """
    owner_email = serializers.EmailField(source='owner.email', read_only=True)
    owner_name = serializers.SerializerMethodField()
    owner_id = serializers.IntegerField(source='owner.id', read_only=True)

    class Meta:
        model = Pet
        fields = [
            'id',
            'owner',
            'owner_id',
            'owner_email',
            'owner_name',
            'name',
            'breed',
            'age',
            'weight',
            'gender',
            'pet_type',
            'date_of_birth',
            'color',
            'profile_picture',
            'microchip_number',
            'notes',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'owner',
            'owner_id',
            'owner_email',
            'owner_name',
            'created_at',
            'updated_at',
        ]

    def get_owner_name(self, obj):
        """
        Return owner's full name.
        """
        return obj.owner.get_full_name()
